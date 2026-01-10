import httpx
from datetime import datetime, timezone, timedelta
from typing import Optional, List
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

    async def get_forecast(self, lat: float, lon: float, hours: int = 12) -> List[WeatherData]:
        """
        Obtiene pronóstico para las próximas N horas
        """
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "wave_height,wind_speed_10m,wind_direction_10m",
            "timezone": "America/Argentina/Buenos_Aires",
            "forecast_days": 2  # Pedimos 2 días para asegurar cobertura
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
        return await self._parse_forecast_response(data, lat, lon, hours)

    async def _parse_response(self, data: dict, lat: float, lon: float) -> WeatherData:
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])
        
        if not times:
            raise ValueError("No se recibieron datos de OpenMeteo")
            
        # Encontrar índice actual
        current_idx = self._find_current_index(times)
        
        tide_state = await self._get_tide_state(lat, lon)
        
        return self._extract_weather_data(hourly, current_idx, tide_state)

    async def _parse_forecast_response(self, data: dict, lat: float, lon: float, limit_hours: int) -> List[WeatherData]:
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])
        
        if not times:
            return []
            
        start_idx = self._find_current_index(times)
        result = []
        
        # Obtener marea una sola vez (idealmente debería ser por hora, pero simplificamos por API limits)
        # TODO: Mejorar predicción de marea horaria
        tide_state = await self._get_tide_state(lat, lon)
        
        for i in range(start_idx, min(start_idx + limit_hours, len(times))):
            wd = self._extract_weather_data(hourly, i, tide_state)
            result.append(wd)
            
        return result

    def _find_current_index(self, times: List[str]) -> int:
        now = datetime.now() # OpenMeteo devuelve local time según timezone parameter
        # Como pedimos America/Argentina/Buenos_Aires, 'now' debe ser naive local o aware convertido
        # Simplificación: Buscar string más cercano o asumir que API devuelve desde 00:00 hoy
        # La API devuelve ISO strings. Vamos a buscar el más cercano a 'now' UTC convertido a str
        # OpenMeteo time es ISO8601 sin offset si timezone es auto o local
        
        # Hack simple: Iterar y comparar. Optimizable.
        current_hour = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:00")
        # Esto es complejo por las timezones. 
        # Mejor approach: Asumimos que el primer index es 00:00 local hoy.
        # Calculamos hora local actual.
        
        # Simplificación robusta: Parsear primera fecha, calcular diferencia horas.
        try:
            first_time = datetime.fromisoformat(times[0])
            # Asumimos que times[0] es local time
            now_local = datetime.now(timezone(timedelta(hours=-3))) # Argentina
            diff = int((now_local.replace(tzinfo=None) - first_time).total_seconds() / 3600)
            return max(0, diff)
        except:
            return 0

    async def _get_tide_state(self, lat, lon) -> str:
        if self.worldtides_provider:
            try:
                return await self.worldtides_provider.get_tide_state(lat, lon)
            except:
                return "rising"
        return "rising"

    def _extract_weather_data(self, hourly: dict, index: int, tide_state: str) -> WeatherData:
        times = hourly.get("time", [])
        if index >= len(times):
            index = len(times) - 1
            
        wind_speed = hourly.get("wind_speed_10m", [])[index]
        wind_direction = hourly.get("wind_direction_10m", [])[index]
        wave_height = hourly.get("wave_height", [])[index]
        timestamp = times[index]
        
        wind_data = WindData(
            speed_kmh=float(wind_speed) if wind_speed is not None else 0.0,
            direction_deg=int(wind_direction) if wind_direction is not None else 0,
            relative_direction=None
        )
        
        wave_data = WaveData(
            height_m=float(wave_height) if wave_height is not None else 0.0
        )
        
        tide_data = TideData(state=tide_state)
        
        return WeatherData(
            wind=wind_data,
            waves=wave_data,
            tide=tide_data,
            timestamp=timestamp,
            provider="openmeteo"
        )
