import httpx
import os
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from app.services.weather_service import WeatherProvider
from app.models.schemas import WeatherData, WindData, WaveData, TideData, AtmosphereData

logger = logging.getLogger(__name__)

class OpenWeatherProvider(WeatherProvider):
    """
    Proveedor de datos usando OpenWeatherMap API (Plan Gratuito)
    Docs: https://openweathermap.org/forecast5
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
                # Re-lanzar para que el HybridProvider use fallback
                raise

    async def get_forecast(self, lat: float, lon: float, hours: int = 24) -> List[WeatherData]:
        """Obtiene pronóstico 3-horario (5 days)"""
        if not self.api_key:
            raise ValueError("API Key faltante")
            
        async with httpx.AsyncClient() as client:
            try:
                params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "metric",
                    "cnt": int(hours / 3) + 2  # Pedir suficientes puntos (cada punto es 3hs)
                }
                response = await client.get(f"{self.BASE_URL}/forecast", params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                result = []
                # El endpoint retorna lista "list"
                for item in data.get("list", []):
                    wd = self._map_to_weather_data(item)
                    result.append(wd)
                    
                    # Interpolar horas intermedias?
                    # Por simplicidad, OpenWeather ofrece datos cada 3hs en free tier.
                    # Para tener hora a hora, podríamos repetir o interpolar.
                    # Vamos a implementar una repetición simple para llenar los huecos 
                    # si es necesario, o dejar que el sistema use puntos cada 3hs.
                    # El sistema espera hora a hora.
                    
                    # Generar +1h y +2h clonados (interpolación simple sticky)
                    # Esto es un "hack" para llenar la timeline horaria con datos 3-horarios
                    current_ts = datetime.fromisoformat(wd.timestamp)
                    for offset in range(1, 3):
                         # Clonar data pero cambiar timestamp
                        next_ts = current_ts + timedelta(hours=offset)
                        wd_clone = wd.model_copy(deep=True)
                        wd_clone.timestamp = next_ts.isoformat()
                        result.append(wd_clone)
                
                # Filtrar y ordenar por timestamp, cortar a 'hours' length
                result.sort(key=lambda x: x.timestamp)
                return result[:hours]

            except Exception as e:
                logger.error(f"Error fetching OpenWeather forecast: {e}")
                raise

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
        wind_speed = wind.get("speed") # m/s
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
