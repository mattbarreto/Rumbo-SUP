from datetime import datetime, timezone, timedelta
from typing import Optional, List
from app.services.weather_service import WeatherProvider
from app.services.http_client import http_client
from app.models.schemas import WeatherData, WindData, WaveData, TideData, AtmosphereData
import logging

logger = logging.getLogger(__name__)

class OpenMeteoProvider(WeatherProvider):
    """
    Implementación de WeatherProvider para OpenMeteo
    
    ARQUITECTURA DE DATOS REALES:
    - Weather Forecast API: viento (funciona en Mar del Plata)
    - Marine API: olas (funciona en océanos)
    - Combina ambos para datos completos
    
    ROBUSTEZ:
    - Fallback si una API falla
    - Validación de índices
    - Manejo correcto de timezones
    """
    
    MARINE_URL = "https://marine-api.open-meteo.com/v1/marine"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self, tide_provider=None):
        """
        Args:
            tide_provider: Opcional - provider para datos de marea (NOAA, WorldTides, etc)
        """
        self.tide_provider = tide_provider
    
    async def get_conditions(self, lat: float, lon: float) -> WeatherData:
        """
        Obtiene datos REALES combinando dos APIs de OpenMeteo:
        1. Weather Forecast API -> viento (tiene datos para Mar del Plata)
        2. Marine API -> olas (tiene datos oceánicos)
        """
        forecast_data = None
        marine_data = None
        
        # Request 1: Viento desde Weather Forecast API
        try:
            forecast_data = await self._fetch_forecast_data(lat, lon)
            if forecast_data:
                hourly = forecast_data.get("hourly", {})
                times = hourly.get("time", [])
                logger.info(f"✅ Forecast API: {len(times)} horas, keys={list(hourly.keys())}")
            else:
                logger.warning("⚠️ Forecast API retornó None")
        except Exception as e:
            logger.error(f"❌ Forecast API failed: {e}")
            # Continuar - intentaremos obtener datos parciales
        
        # Request 2: Olas desde Marine API
        try:
            marine_data = await self._fetch_marine_data(lat, lon)
            if marine_data:
                hourly = marine_data.get("hourly", {})
                times = hourly.get("time", [])
                logger.info(f"✅ Marine API: {len(times)} horas, keys={list(hourly.keys())}")
            else:
                logger.warning("⚠️ Marine API retornó None")
        except Exception as e:
            logger.error(f"❌ Marine API failed: {e}")
            # Continuar - intentaremos obtener datos parciales
        
        # Verificar que al menos una API funcionó CON DATOS
        has_forecast_data = forecast_data and forecast_data.get("hourly", {}).get("time", [])
        has_marine_data = marine_data and marine_data.get("hourly", {}).get("time", [])
        
        if not has_forecast_data and not has_marine_data:
            raise ValueError("OpenMeteo: Ambas APIs retornaron datos vacíos")
        
        # Combinar ambos resultados (con fallbacks)
        return await self._parse_combined_response(forecast_data, marine_data, lat, lon)


    async def get_forecast(self, lat: float, lon: float, hours: int = 12) -> List[WeatherData]:
        """
        Obtiene pronóstico REAL para las próximas N horas
        Combina Weather Forecast API (viento) + Marine API (olas)
        """
        forecast_data = None
        marine_data = None
        
        # Request 1: Viento
        try:
            forecast_params = {
                "latitude": lat,
                "longitude": lon,
                "hourly": "wind_speed_10m,wind_direction_10m,temperature_2m,precipitation,weathercode,cloudcover,uv_index,visibility",
                "timezone": "UTC",
                "forecast_days": 2,
                "models": "best_match"
            }
            # Usa http_client.get que ya valida status y hace retries
            forecast_response_json = await http_client.get(
                self.FORECAST_URL,
                params=forecast_params
            )
            forecast_data = forecast_response_json
        except Exception as e:
            logger.error(f"Forecast API forecast failed: {e}")
        
        # Request 2: Olas
        try:
            marine_params = {
                "latitude": lat,
                "longitude": lon,
                "hourly": "wave_height,wave_period,wave_direction",
                "timezone": "UTC",
                "forecast_days": 2
            }
            marine_response_json = await http_client.get(
                self.MARINE_URL,
                params=marine_params
            )
            marine_data = marine_response_json
        except Exception as e:
            logger.error(f"Marine API forecast failed: {e}")
        
        # Validar que al menos un API retornó datos reales
        has_forecast_data = forecast_data and forecast_data.get("hourly", {}).get("time", [])
        has_marine_data = marine_data and marine_data.get("hourly", {}).get("time", [])
        
        if has_forecast_data:
            logger.info(f"✅ Forecast API forecast: {len(forecast_data['hourly']['time'])} horas")
        if has_marine_data:
            logger.info(f"✅ Marine API forecast: {len(marine_data['hourly']['time'])} horas")
            
        if not has_forecast_data and not has_marine_data:
            raise ValueError("OpenMeteo Forecast: Ambas APIs retornaron datos vacíos")
            
        return await self._parse_combined_forecast_response(forecast_data, marine_data, lat, lon, hours)

    async def _parse_combined_response(self, forecast_data: Optional[dict], marine_data: Optional[dict], lat: float, lon: float) -> WeatherData:
        """Combina datos de viento (forecast) y olas (marine) en WeatherData"""
        # Usar datos de forecast si están disponibles, sino crear estructura vacía
        forecast_hourly = forecast_data.get("hourly", {}) if forecast_data else {}
        marine_hourly = marine_data.get("hourly", {}) if marine_data else {}
        
        # Intentar obtener times del forecast primero, sino del marine
        times = forecast_hourly.get("time", []) or marine_hourly.get("time", [])
        
        if not times:
            # Fallback completo: crear datos con valores actuales
            logger.warning("No hay datos de tiempo disponibles, usando valores por defecto")
            return self._create_fallback_weather_data(lat, lon)
            
        # Encontrar índice actual
        current_idx = self._find_current_index(times)
        
        # Obtener estado de marea
        tide_state = await self._get_tide_state(lat, lon)
        
        # Extraer datos combinados
        return self._extract_combined_weather_data(forecast_hourly, marine_hourly, current_idx, tide_state)

    async def _parse_combined_forecast_response(self, forecast_data: Optional[dict], marine_data: Optional[dict], lat: float, lon: float, limit_hours: int) -> List[WeatherData]:
        """Combina forecast de viento y olas para múltiples horas"""
        forecast_hourly = forecast_data.get("hourly", {}) if forecast_data else {}
        marine_hourly = marine_data.get("hourly", {}) if marine_data else {}
        
        times = forecast_hourly.get("time", []) or marine_hourly.get("time", [])
        
        if not times:
            logger.warning("No hay datos de pronóstico disponibles")
            return []
            
        start_idx = self._find_current_index(times)
        result = []
        
        # Obtener marea una sola vez
        tide_state = await self._get_tide_state(lat, lon)
        
        # Calcular hasta dónde podemos iterar
        max_idx = min(start_idx + limit_hours, len(times))
        
        for i in range(start_idx, max_idx):
            relative_offset = i - start_idx
            wd = self._extract_combined_weather_data(forecast_hourly, marine_hourly, i, tide_state, hour_offset=relative_offset)
            result.append(wd)
            
        return result

    def _extract_combined_weather_data(self, forecast_hourly: dict, marine_hourly: dict, index: int, tide_state: str, hour_offset: int = 0) -> WeatherData:
        """Extrae y combina datos de viento (forecast) y olas (marine) para un índice específico - CON VALIDACIÓN"""
        forecast_times = forecast_hourly.get("time", [])
        
        # Validar índice contra la longitud real de los arrays
        if index >= len(forecast_times) and len(forecast_times) > 0:
            index = len(forecast_times) - 1
        elif len(forecast_times) == 0:
            # Fallback total si no hay datos - usar offset para generar timestamp secuencial
            logger.warning(f"No hay datos de tiempo en forecast para índice {index}")
            return self._create_fallback_weather_data(0, 0, tide_state, hour_offset=hour_offset)
        
        # Timestamp siempre viene del forecast (o marine como fallback)
        # Aseguramos que tenga la marca Z de UTC si no la tiene
        raw_ts = forecast_times[index] if forecast_times else datetime.now(timezone.utc).isoformat()
        if not raw_ts.endswith("Z") and "+00:00" not in raw_ts:
             timestamp = f"{raw_ts}Z"
        else:
             timestamp = raw_ts
        
        # Helper para extracción segura
        def get_val(source, key, idx, type_func=float):
            arr = source.get(key, [])
            if idx < len(arr) and arr[idx] is not None:
                try:
                    return type_func(arr[idx])
                except (ValueError, TypeError):
                    return None
            return None

        # --- Viento ---
        wind_speed = get_val(forecast_hourly, "wind_speed_10m", index)
        wind_direction = get_val(forecast_hourly, "wind_direction_10m", index, int)
        
        # --- Olas (Marine) ---
        wave_height = get_val(marine_hourly, "wave_height", index)
        wave_period = get_val(marine_hourly, "wave_period", index)
        wave_direction = get_val(marine_hourly, "wave_direction", index, int)
        
        # --- Atmósfera (Forecast) ---
        temp = get_val(forecast_hourly, "temperature_2m", index)
        precip = get_val(forecast_hourly, "precipitation", index)
        clouds = get_val(forecast_hourly, "cloudcover", index, int)
        uv = get_val(forecast_hourly, "uv_index", index)
        visibility = get_val(forecast_hourly, "visibility", index)
        # Convertir visibilidad de metros a km si es necesario (OpenMeteo da metros)
        if visibility is not None:
            visibility = visibility / 1000.0
            
        wcode = get_val(forecast_hourly, "weathercode", index, int)

        # Construir objetos
        wind_data = WindData(
            speed_kmh=wind_speed,
            direction_deg=wind_direction,
            relative_direction=None
        )
        
        wave_data = WaveData(
            height_m=wave_height,
            period_s=wave_period,
            direction_deg=wave_direction
        )
        
        atmosphere_data = AtmosphereData(
            temperature_c=temp,
            precipitation_mm=precip,
            cloud_cover_pct=clouds,
            uv_index=uv,
            visibility_km=visibility,
            weather_code=wcode
        )
        
        tide_data = TideData(state=tide_state)
        
        return WeatherData(
            wind=wind_data,
            waves=wave_data,
            atmosphere=atmosphere_data,
            tide=tide_data,
            timestamp=timestamp,
            provider="openmeteo_combined"
        )

    def _find_current_index(self, times: List[str]) -> int:
        """Encuentra el índice de la hora actual usando UTC de forma estricta.
        
        Compara datetime.now(timezone.utc) contra los timestamps de la API (también en UTC).
        """
        if not times:
            return 0
            
        try:
            # 1. Obtener ahora en UTC estricto, truncado a la hora para comparar bloques
            # Ejemplo: Si son 11:48 UTC, buscamos el bloque de las 11:00 UTC
            now_utc = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
            
            # Buscar la primera hora >= la hora actual
            for i, time_str in enumerate(times):
                # OpenMeteo UTC devuelve ISO8601 (ej: "2026-01-14T14:00")
                # Lo parseamos y le asignamos timezone UTC explícitamente para comparar peras con peras
                entry_time = datetime.fromisoformat(time_str.split('+')[0].split('Z')[0]).replace(tzinfo=timezone.utc)
                
                # Si encontramos el bloque actual (igualdad) o uno futuro (mayor)
                if entry_time >= now_utc:
                    return i
            
            return len(times) - 1
            
        except Exception as e:
            logger.error(f"Error calculando índice de tiempo: {e}")
            return 0

    def _create_fallback_weather_data(self, lat: float, lon: float, tide_state: str = "rising", hour_offset: int = 0) -> WeatherData:
        """Crea WeatherData con valores None pero con timestamp secuencial correcto"""
        # Generar timestamp basado en hora actual + offset
        now_utc = datetime.now(timezone.utc)
        target_time = now_utc + timedelta(hours=hour_offset)
        
        return WeatherData(
            wind=WindData(speed_kmh=None, direction_deg=None, relative_direction=None),
            waves=WaveData(height_m=None, period_s=None, direction_deg=None),
            atmosphere=AtmosphereData(),
            tide=TideData(state=tide_state),
            timestamp=target_time.isoformat(),
            provider="openmeteo_fallback"
        )
        
    async def _fetch_forecast_data(self, lat, lon):
        """Helper para Forecast API usando ResilientHttpClient"""
        forecast_params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "wind_speed_10m,wind_direction_10m,temperature_2m,precipitation,weathercode,cloudcover,uv_index,visibility",
            "timezone": "UTC",
            "forecast_days": 1,
            "models": "best_match"
        }
        # Delegamos retry/timeout a http_client
        return await http_client.get(self.FORECAST_URL, params=forecast_params)
        
    async def _fetch_marine_data(self, lat, lon):
        """Helper para Marine API usando ResilientHttpClient"""
        marine_params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "wave_height,wave_period,wave_direction",
            "timezone": "UTC",
            "forecast_days": 1
        }
        return await http_client.get(self.MARINE_URL, params=marine_params)

    async def _get_tide_state(self, lat, lon) -> str:
        if self.tide_provider:
            try:
                return await self.tide_provider.get_tide_state(lat, lon)
            except Exception as e:
                logger.error(f"Tide provider error: {e}")
                return "rising"
        return "rising"
