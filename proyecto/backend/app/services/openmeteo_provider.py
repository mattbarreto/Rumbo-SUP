import httpx
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from app.services.weather_service import WeatherProvider
from app.models.schemas import WeatherData, WindData, WaveData, TideData

class OpenMeteoProvider(WeatherProvider):
    """
    Implementación de WeatherProvider para OpenMeteo
    
    ARQUITECTURA DE DATOS REALES:
    - Weather Forecast API: viento (funciona en Mar del Plata)
    - Marine API: olas (funciona en océanos)
    - Combina ambos para datos completos
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
        async with httpx.AsyncClient() as client:
            # Request 1: Viento desde Weather Forecast API
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
            forecast_data = forecast_response.json()
            
            # Request 2: Olas desde Marine API
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
            marine_data = marine_response.json()
        
        # Combinar ambos resultados
        return await self._parse_combined_response(forecast_data, marine_data, lat, lon)

    async def get_forecast(self, lat: float, lon: float, hours: int = 12) -> List[WeatherData]:
        """
        Obtiene pronóstico REAL para las próximas N horas
        Combina Weather Forecast API (viento) + Marine API (olas)
        """
        async with httpx.AsyncClient() as client:
            # Request 1: Viento
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
            
            # Request 2: Olas
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
            
        return await self._parse_combined_forecast_response(forecast_data, marine_data, lat, lon, hours)

    async def _parse_combined_response(self, forecast_data: dict, marine_data: dict, lat: float, lon: float) -> WeatherData:
        """Combina datos de viento (forecast) y olas (marine) en WeatherData"""
        forecast_hourly = forecast_data.get("hourly", {})
        marine_hourly = marine_data.get("hourly", {})
        
        times = forecast_hourly.get("time", [])
        if not times:
            raise ValueError("No se recibieron datos de OpenMeteo Forecast")
            
        # Encontrar índice actual
        current_idx = self._find_current_index(times)
        
        # Obtener estado de marea
        tide_state = await self._get_tide_state(lat, lon)
        
        # Extraer datos combinados
        return self._extract_combined_weather_data(forecast_hourly, marine_hourly, current_idx, tide_state)

    async def _parse_combined_forecast_response(self, forecast_data: dict, marine_data: dict, lat: float, lon: float, limit_hours: int) -> List[WeatherData]:
        """Combina forecast de viento y olas para múltiples horas"""
        forecast_hourly = forecast_data.get("hourly", {})
        marine_hourly = marine_data.get("hourly", {})
        
        times = forecast_hourly.get("time", [])
        if not times:
            return []
            
        start_idx = self._find_current_index(times)
        result = []
        
        # Obtener marea una sola vez
        tide_state = await self._get_tide_state(lat, lon)
        
        for i in range(start_idx, min(start_idx + limit_hours, len(times))):
            wd = self._extract_combined_weather_data(forecast_hourly, marine_hourly, i, tide_state)
            result.append(wd)
            
        return result

    def _extract_combined_weather_data(self, forecast_hourly: dict, marine_hourly: dict, index: int, tide_state: str) -> WeatherData:
        """Extrae y combina datos de viento (forecast) y olas (marine) para un índice específico"""
        forecast_times = forecast_hourly.get("time", [])
        marine_times = marine_hourly.get("time", [])
        
        if index >= len(forecast_times):
            index = len(forecast_times) - 1
        
        # Viento desde Forecast API
        wind_speed = forecast_hourly.get("wind_speed_10m", [])[index]
        wind_direction = forecast_hourly.get("wind_direction_10m", [])[index]
        timestamp = forecast_times[index]
        
        # Olas desde Marine API (mismo índice, mismas horas)
        wave_height = marine_hourly.get("wave_height", [])[index] if index < len(marine_hourly.get("wave_height", [])) else 0.0
        
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
            provider="openmeteo_combined"
        )

    def _find_current_index(self, times: List[str]) -> int:
        """Encuentra el índice de la hora actual en el array de tiempos"""
        try:
            first_time = datetime.fromisoformat(times[0])
            now_local = datetime.now(timezone(timedelta(hours=-3)))  # Argentina UTC-3
            diff = int((now_local.replace(tzinfo=None) - first_time).total_seconds() / 3600)
            return max(0, diff)
        except:
            return 0

    async def _get_tide_state(self, lat, lon) -> str:
        if self.tide_provider:
            try:
                return await self.tide_provider.get_tide_state(lat, lon)
            except:
                return "rising"
        return "rising"
