import httpx
from datetime import datetime, timezone
from typing import Optional
from app.services.weather_service import WeatherProvider
from app.models.schemas import WeatherData, WindData, WaveData, TideData

class OpenMeteoProvider(WeatherProvider):
    """
    Implementación de WeatherProvider para OpenMeteo Marine API
    API gratuita, sin necesidad de API key
    """
    
    BASE_URL = "https://marine-api.open-meteo.com/v1/marine"
    
    def __init__(self, worldtides_provider=None):
        """
        Args:
            worldtides_provider: Opcional - provider para datos de marea
        """
        self.worldtides_provider = worldtides_provider
    
    async def get_conditions(self, lat: float, lon: float) -> WeatherData:
        """
        Obtiene datos de OpenMeteo Marine API
        """
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "wave_height,wind_speed_10m,wind_direction_10m",
            "timezone": "America/Argentina/Buenos_Aires",
            "forecast_days": 1
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        
        # Parsear respuesta
        return await self._parse_response(data, lat, lon)
    
    async def _parse_response(self, data: dict, lat: float, lon: float) -> WeatherData:
        """
        Parsea respuesta de OpenMeteo a nuestro formato interno
        """
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])
        
        if not times:
            raise ValueError("No se recibieron datos de OpenMeteo")
        
        # Obtener índice de la hora más cercana a ahora
        now = datetime.now(timezone.utc)
        current_index = 0  # Primera hora disponible (usualmente la actual)
        
        # Extraer datos de la hora actual
        wind_speed = hourly.get("wind_speed_10m", [])[current_index]
        wind_direction = hourly.get("wind_direction_10m", [])[current_index]
        wave_height = hourly.get("wave_height", [])[current_index]
        
        # Convertir a nuestros modelos
        wind_data = WindData(
            speed_kmh=float(wind_speed) if wind_speed is not None else 0.0,
            direction_deg=int(wind_direction) if wind_direction is not None else 0,
            relative_direction=None  # Se calcula después con orientación del spot
        )
        
        wave_data = WaveData(
            height_m=float(wave_height) if wave_height is not None else 0.0
        )
        
        # Marea: usar WorldTides si está disponible
        if self.worldtides_provider:
            try:
                tide_state = await self.worldtides_provider.get_tide_state(lat, lon)
                tide_data = TideData(state=tide_state)
            except Exception as e:
                print(f"Error getting WorldTides data: {e}")
                tide_data = TideData(state="rising")  # Fallback
        else:
            # Sin WorldTides, usar placeholder
            tide_data = TideData(state="rising")
        
        return WeatherData(
            wind=wind_data,
            waves=wave_data,
            tide=tide_data,
            timestamp=times[current_index],
            provider="openmeteo+worldtides" if self.worldtides_provider else "openmeteo"
        )
