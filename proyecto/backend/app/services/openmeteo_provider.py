import httpx
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from app.services.weather_service import WeatherProvider
from app.models.schemas import WeatherData, WindData, WaveData, TideData
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

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
        
        async with httpx.AsyncClient() as client:
            # Request 1: Viento desde Weather Forecast API
            try:
                forecast_data = await self._fetch_forecast_data(client, lat, lon)
                logger.info("✅ Forecast API: datos de viento obtenidos")
            except Exception as e:
                logger.error(f"❌ Forecast API failed: {e}")
                # Continuar - intentaremos obtener datos parciales
            
            # Request 2: Olas desde Marine API
            try:
                marine_data = await self._fetch_marine_data(client, lat, lon)
                logger.info("✅ Marine API: datos de olas obtenidos")
            except Exception as e:
                logger.error(f"❌ Marine API failed: {e}")
                # Continuar - intentaremos obtener datos parciales
        
        # Verificar que al menos una API funcionó
        if forecast_data is None and marine_data is None:
            raise ValueError("Ambas APIs de OpenMeteo fallaron - no hay datos disponibles")
        
        # Combinar ambos resultados (con fallbacks)
        return await self._parse_combined_response(forecast_data, marine_data, lat, lon)

    async def get_forecast(self, lat: float, lon: float, hours: int = 12) -> List[WeatherData]:
        """
        Obtiene pronóstico REAL para las próximas N horas
        Combina Weather Forecast API (viento) + Marine API (olas)
        """
        forecast_data = None
        marine_data = None
        
        async with httpx.AsyncClient() as client:
            # Request 1: Viento
            try:
                forecast_params = {
                    "latitude": lat,
                    "longitude": lon,
                    "hourly": "wind_speed_10m,wind_direction_10m",
                    "timezone": "America/Argentina/Buenos_Aires",
                    "forecast_days": 2
                }
                forecast_response = await client.get(
                    self.FORECAST_URL,
                    params=forecast_params,
                    timeout=10.0
                )
                forecast_response.raise_for_status()
                forecast_data = forecast_response.json()
            except Exception as e:
                logger.error(f"Forecast API forecast failed: {e}")
            
            # Request 2: Olas
            try:
                marine_params = {
                    "latitude": lat,
                    "longitude": lon,
                    "hourly": "wave_height",
                    "timezone": "America/Argentina/Buenos_Aires",
                    "forecast_days": 2
                }
                marine_response = await client.get(
                    self.MARINE_URL,
                    params=marine_params,
                    timeout=10.0
                )
                marine_response.raise_for_status()
                marine_data = marine_response.json()
            except Exception as e:
                logger.error(f"Marine API forecast failed: {e}")
            
        if forecast_data is None and marine_data is None:
            raise ValueError("Ambas APIs fallaron - no se puede obtener pronóstico")
            
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
            wd = self._extract_combined_weather_data(forecast_hourly, marine_hourly, i, tide_state)
            result.append(wd)
            
        return result

    def _extract_combined_weather_data(self, forecast_hourly: dict, marine_hourly: dict, index: int, tide_state: str) -> WeatherData:
        """Extrae y combina datos de viento (forecast) y olas (marine) para un índice específico - CON VALIDACIÓN"""
        forecast_times = forecast_hourly.get("time", [])
        
        # Validar índice contra la longitud real de los arrays
        if index >= len(forecast_times) and len(forecast_times) > 0:
            index = len(forecast_times) - 1
        elif len(forecast_times) == 0:
            # Fallback total si no hay datos
            logger.warning(f"No hay datos de tiempo en forecast para índice {index}")
            return self._create_fallback_weather_data(0, 0, tide_state)
        
        # Timestamp siempre viene del forecast (o marine como fallback)
        timestamp = forecast_times[index] if forecast_times else datetime.now(timezone.utc).isoformat()
        
        # Obtener viento desde Forecast API (CON VALIDACIÓN)
        wind_speeds = forecast_hourly.get("wind_speed_10m", [])
        wind_directions = forecast_hourly.get("wind_direction_10m", [])
        
        wind_speed = wind_speeds[index] if index < len(wind_speeds) else None
        wind_direction = wind_directions[index] if index < len(wind_directions) else None
        
        # Obtener olas desde Marine API (CON VALIDACIÓN)
        wave_heights = marine_hourly.get("wave_height", [])
        wave_height = wave_heights[index] if index < len(wave_heights) else None
        
        # Crear objetos con None si no hay datos (cliente maneja el "N/A")
        wind_data = WindData(
            speed_kmh=float(wind_speed) if wind_speed is not None else None,
            direction_deg=int(wind_direction) if wind_direction is not None else None,
            relative_direction=None
        )
        
        wave_data = WaveData(
            height_m=float(wave_height) if wave_height is not None else None
        )
        
        tide_data = TideData(state=tide_state)
        
        return WeatherData(
            wind=wind_data,
            waves=wave_data,
            tide=tide_data,
            timestamp=timestamp,
            provider="openmeteo_combined"
        )

    def _find_current_index(self, times: List[str]) -> int:
        """Encuentra el índice de la hora actual en el array de tiempos - MEJORADO"""
        if not times:
            return 0
            
        try:
            # Parsear el primer timestamp
            first_time_str = times[0]
            
            # OpenMeteo con timezone devuelve formato: "2024-01-13T14:00"
            # Intentar parsear como naive primero
            if 'T' in first_time_str:
                # Formato ISO sin timezone
                first_time = datetime.fromisoformat(first_time_str.replace('Z', '+00:00'))
            else:
                # Fallback
                first_time = datetime.fromisoformat(first_time_str)
            
            # Hacer first_time naive si tiene tzinfo
            if first_time.tzinfo:
                first_time = first_time.replace(tzinfo=None)
            
            # Obtener hora actual en Argentina (UTC-3) como naive
            now_utc = datetime.now(timezone.utc)
            now_argentina = now_utc - timedelta(hours=3)
            now_naive = now_argentina.replace(tzinfo=None)
            
            # Calcular diferencia en horas
            diff_seconds = (now_naive - first_time).total_seconds()
            diff_hours = int(diff_seconds / 3600)
            
            # Retornar índice válido (no negativo, no mayor que len)
            return max(0, min(diff_hours, len(times) - 1))
            
        except Exception as e:
            logger.error(f"Error calculando índice de tiempo: {e}")
            return 0

    def _create_fallback_weather_data(self, lat: float, lon: float, tide_state: str = "rising") -> WeatherData:
        """Crea WeatherData con valores None para indicar falta de datos"""
        return WeatherData(
            wind=WindData(speed_kmh=None, direction_deg=None, relative_direction=None),
            waves=WaveData(height_m=None),
            tide=TideData(state=tide_state),
            timestamp=datetime.now(timezone.utc).isoformat(),
            provider="openmeteo_fallback"
        )
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), retry=retry_if_exception_type(httpx.TransportError))
    async def _fetch_forecast_data(self, client, lat, lon):
        """Helper con retry para Forecast API"""
        forecast_params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "wind_speed_10m,wind_direction_10m",
            "timezone": "America/Argentina/Buenos_Aires",
            "forecast_days": 1
        }
        forecast_response = await client.get(
            self.FORECAST_URL,
            params=forecast_params,
            timeout=10.0
        )
        forecast_response.raise_for_status()
        return forecast_response.json()
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), retry=retry_if_exception_type(httpx.TransportError))
    async def _fetch_marine_data(self, client, lat, lon):
        """Helper con retry para Marine API"""
        marine_params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "wave_height",
            "timezone": "America/Argentina/Buenos_Aires",
            "forecast_days": 1
        }
        marine_response = await client.get(
            self.MARINE_URL,
            params=marine_params,
            timeout=10.0
        )
        marine_response.raise_for_status()
        return marine_response.json()

    async def _get_tide_state(self, lat, lon) -> str:
        if self.tide_provider:
            try:
                return await self.tide_provider.get_tide_state(lat, lon)
            except Exception as e:
                logger.error(f"Tide provider error: {e}")
                return "rising"
        return "rising"
