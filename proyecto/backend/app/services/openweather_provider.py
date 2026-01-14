import httpx
import os
import logging
import asyncio
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from app.services.weather_service import WeatherProvider
from app.models.schemas import WeatherData, WindData, WaveData, TideData, AtmosphereData

logger = logging.getLogger(__name__)

class OpenWeatherProvider(WeatherProvider):
    """
    Proveedor de datos usando OpenWeatherMap API (Plan Gratuito)
    Docs: https://openweathermap.org/forecast5
    Estrategia de Tiempo: Combina /weather (Current) + /forecast (3-hour steps)
    para asegurar continuidad desde la hora actual.
    """
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            logger.warning("OPENWEATHER_API_KEY no configurada. El proveedor fallará.")
            
    async def get_conditions(self, lat: float, lon: float) -> WeatherData:
        """Obtiene condiciones actuales usando endpoint /weather"""
        if not self.api_key:
            raise ValueError("API Key faltante")
            
        async with httpx.AsyncClient() as client:
            try:
                params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "metric"
                }
                response = await client.get(f"{self.BASE_URL}/weather", params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                return self._map_to_weather_data(data)
            except Exception as e:
                logger.error(f"Error fetching OpenWeather conditions: {e}")
                raise

    async def get_forecast(self, lat: float, lon: float, hours: int = 24) -> List[WeatherData]:
        """Obtiene pronóstico combinando Current + Forecast para asegurar inicio en hora actual"""
        if not self.api_key:
            raise ValueError("API Key faltante")
            
        # 1. Ejecutar Current y Forecast SECUENCIALMENTE para evitar rate limits o bloqueos
        # Current es crítico para el punto de partida (Hora actual)
        current_wd = None
        forecast_list = []
        
        try:
             # Fetch Current
             current_wd = await self.get_conditions(lat, lon)
             logger.info(f"✅ DEBUG: Current weather fetch success: {current_wd.timestamp}")
        except Exception as e:
             logger.error(f"❌ DEBUG: Current weather fetch failed: {e}")
             current_wd = None
             
        try:
             # Fetch Forecast
             forecast_list = await self._fetch_raw_forecast(lat, lon, hours)
             logger.info(f"✅ DEBUG: Forecast list fetch success: {len(forecast_list)} items")
        except Exception as e:
             logger.error(f"❌ DEBUG: Forecast fetch failed: {e}")
             if current_wd: return [current_wd] # Devolver al menos lo que tenemos
             raise e
            
        # 2. Procesar Forecast (Interpolación 3h -> 1h)
        processed_forecast = []
        for wd in forecast_list:
            processed_forecast.append(wd)
            # Rellenar huecos hacia adelante (3h steps -> 1h steps)
            current_ts = datetime.fromisoformat(wd.timestamp.replace("Z", "+00:00"))
            for offset in range(1, 3):
                next_ts = current_ts + timedelta(hours=offset)
                wd_clone = wd.model_copy(deep=True)
                wd_clone.timestamp = next_ts.isoformat()
                processed_forecast.append(wd_clone)
        
        # Ordenar forecast procesado
        processed_forecast.sort(key=lambda x: x.timestamp)
        
        # 3. Integrar CurrentWeather al inicio
        final_list = []
        
        if current_wd:
            # Normalizar current timestamp al inicio de la hora exacta
            # Ej: 15:48 -> 15:00
            curr_dt = datetime.fromisoformat(current_wd.timestamp.replace("Z", "+00:00"))
            curr_hour = curr_dt.replace(minute=0, second=0, microsecond=0)
            current_wd.timestamp = curr_hour.isoformat()
            
            final_list.append(current_wd)
            
            # Rellenar hueco entre Current y el primer Forecast
            if processed_forecast:
                first_forecast_dt = datetime.fromisoformat(processed_forecast[0].timestamp.replace("Z", "+00:00"))
                
                # Si hay hueco (ej: Current 15:00, First Forecast 18:00)
                # Rellenar 16:00, 17:00 con datos de Current
                gap_hours = int((first_forecast_dt - curr_hour).total_seconds() / 3600)
                
                for i in range(1, gap_hours):
                    fill_ts = curr_hour + timedelta(hours=i)
                    fill_wd = current_wd.model_copy(deep=True)
                    fill_wd.timestamp = fill_ts.isoformat()
                    final_list.append(fill_wd)
        
        # 4. Combinar con forecast (evitando duplicados de hora)
        # Usamos un set para trackear horas ya agregadas
        seen_hours = set()
        for item in final_list:
            seen_hours.add(item.timestamp)
            
        for item in processed_forecast:
            # Si esta hora ya la cubrimos con Current (o relleno), saltar
            # (Prefers Current data over Forecast data for overlapping hours)
            if item.timestamp not in seen_hours:
                # Solo agregar si es futuro respecto al último que tenemos
                # O simplemente agregar y luego filtrar/ordenar
                final_list.append(item)
                seen_hours.add(item.timestamp)

        # 5. Filtrar items pasados (mantener desde hora actual)
        now_hour = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        final_list = [
            x for x in final_list 
            if datetime.fromisoformat(x.timestamp.replace("Z", "+00:00")) >= now_hour
        ]
        
        final_list.sort(key=lambda x: x.timestamp)
        return final_list[:hours]

    async def _fetch_raw_forecast(self, lat, lon, hours):
        """Helper para obtener solo la lista raw de forecast"""
        async with httpx.AsyncClient() as client:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",
                "cnt": int(hours / 3) + 4 # Pedir extra por si acaso
            }
            response = await client.get(f"{self.BASE_URL}/forecast", params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            result = []
            for item in data.get("list", []):
                result.append(self._map_to_weather_data(item))
            return result

    def _map_to_weather_data(self, data: dict) -> WeatherData:
        """Mapea respuesta JSON de OpenWeather a WeatherData"""
        
        # Timestamp (dt es unix timestamp)
        ts_unix = data.get("dt")
        if ts_unix:
            timestamp = datetime.fromtimestamp(ts_unix, timezone.utc).isoformat()
        else:
            timestamp = datetime.now(timezone.utc).isoformat()
            
        # Viento
        wind = data.get("wind", {})
        wind_speed = wind.get("speed") # m/s (default metric)
        wind_deg = wind.get("deg")
        
        if wind_speed is not None:
            wind_speed_kmh = wind_speed * 3.6
        else:
            wind_speed_kmh = None
            
        # Main info (Temp, Pressure, Humidity)
        main = data.get("main", {})
        temp = main.get("temp")
        
        # Weather (Clouds, Rain)
        weather = data.get("weather", [{}])[0]
        wcode = weather.get("id") # ID WMO standard
        
        clouds = data.get("clouds", {}).get("all")
        
        # Rain (volumen last 1h or 3h)
        rain = data.get("rain", {})
        precip = rain.get("1h", rain.get("3h", 0))
        
        # Visibility (metros)
        vis_m = data.get("visibility")
        vis_km = vis_m / 1000.0 if vis_m is not None else None

        # --- Construcción de Objetos ---
        
        wind_obj = WindData(
            speed_kmh=round(wind_speed_kmh, 1) if wind_speed_kmh is not None else None,
            direction_deg=wind_deg,
            relative_direction=None
        )
        
        # OpenWeather Free NO TIENE OLAS. Devolvemos None.
        wave_obj = WaveData(
            height_m=None,
            period_s=None,
            direction_deg=None
        )
        
        atmosphere_obj = AtmosphereData(
            temperature_c=temp,
            precipitation_mm=precip,
            cloud_cover_pct=clouds,
            uv_index=None, # No disponible en endpoint standard weather/forecast
            visibility_km=vis_km,
            weather_code=wcode
        )
        
        # Tide no disponible
        tide_obj = TideData(state="rising") # Placeholder
        
        return WeatherData(
            wind=wind_obj,
            waves=wave_obj,
            atmosphere=atmosphere_obj,
            tide=tide_obj,
            timestamp=timestamp,
            provider="openweather"
        )
