"""
Stormglass.io Weather Provider

API especializada en datos marinos con alta disponibilidad.
Tier gratuito: 10 requests/día
"""

import httpx
import os
from datetime import datetime, timezone
from typing import List, Optional
from app.services.weather_service import WeatherProvider
from app.models.schemas import WeatherData, WindData, WaveData, TideData
import logging

logger = logging.getLogger(__name__)

class StormglassProvider(WeatherProvider):
    """
    Provider de datos meteorológicos usando Stormglass.io API
    
    VENTAJAS:
    - Alta disponibilidad
    - Datos marinos especializados (olas, swell)
    - Múltiples fuentes de datos
    
    LIMITACIONES:
    - 10 requests/día en tier gratuito
    - Requiere API key
    """
    
    API_URL = "https://api.stormglass.io/v2/weather/point"
    
    def __init__(self, api_key: str = None, tide_provider=None):
        self.api_key = api_key or os.getenv("STORMGLASS_API_KEY")
        self.tide_provider = tide_provider
        
        if not self.api_key:
            logger.warning("⚠️ STORMGLASS_API_KEY not set - provider will fail")
    
    async def get_conditions(self, lat: float, lon: float) -> WeatherData:
        """Obtiene condiciones actuales desde Stormglass"""
        
        if not self.api_key:
            raise ValueError("STORMGLASS_API_KEY not configured")
        
        params = {
            "lat": lat,
            "lng": lon,
            "params": "windSpeed,windDirection,waveHeight,wavePeriod,waveDirection",
            "source": "sg"  # Fuente Stormglass (más confiable)
        }
        
        headers = {
            "Authorization": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.API_URL,
                    params=params,
                    headers=headers,
                    timeout=20.0
                )
                response.raise_for_status()
                data = response.json()
                logger.info("✅ Stormglass API: datos obtenidos")
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 402:
                    logger.error("❌ Stormglass: Límite de requests alcanzado")
                    raise ValueError("Stormglass API limit reached")
                elif e.response.status_code == 401:
                    logger.error("❌ Stormglass: API key inválida")
                    raise ValueError("Stormglass API key invalid")
                else:
                    logger.error(f"❌ Stormglass HTTP error: {e}")
                    raise
            except Exception as e:
                logger.error(f"❌ Stormglass error: {e}")
                raise
        
        return await self._parse_response(data, lat, lon)
    
    async def get_forecast(self, lat: float, lon: float, hours: int = 12) -> List[WeatherData]:
        """Obtiene pronóstico de las próximas horas"""
        
        if not self.api_key:
            raise ValueError("STORMGLASS_API_KEY not configured")
        
        params = {
            "lat": lat,
            "lng": lon,
            "params": "windSpeed,windDirection,waveHeight,wavePeriod,waveDirection",
            "source": "sg"
        }
        
        headers = {
            "Authorization": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.API_URL,
                    params=params,
                    headers=headers,
                    timeout=20.0
                )
                response.raise_for_status()
                data = response.json()
                logger.info("✅ Stormglass API forecast: datos obtenidos")
                
            except Exception as e:
                logger.error(f"❌ Stormglass forecast error: {e}")
                raise
        
        return await self._parse_forecast_response(data, lat, lon, hours)
    
    async def _parse_response(self, data: dict, lat: float, lon: float) -> WeatherData:
        """Parsea respuesta de Stormglass para condiciones actuales"""
        
        hours = data.get("hours", [])
        
        if not hours:
            raise ValueError("No data in Stormglass response")
        
        # Encontrar la hora más cercana al momento actual
        current_hour = self._find_current_hour(hours)
        
        # Obtener marea
        tide_state = await self._get_tide_state(lat, lon)
        
        return self._extract_weather_data(current_hour, tide_state)
    
    async def _parse_forecast_response(self, data: dict, lat: float, lon: float, limit_hours: int) -> List[WeatherData]:
        """Parsea respuesta de Stormglass para forecast"""
        
        hours = data.get("hours", [])
        
        if not hours:
            return []
        
        # Obtener marea
        tide_state = await self._get_tide_state(lat, lon)
        
        result = []
        current_idx = self._find_current_hour_index(hours)
        
        for i in range(current_idx, min(current_idx + limit_hours, len(hours))):
            wd = self._extract_weather_data(hours[i], tide_state)
            result.append(wd)
        
        return result
    
    def _find_current_hour(self, hours: list) -> dict:
        """Encuentra el registro más cercano a la hora actual"""
        now = datetime.now(timezone.utc)
        
        for hour in hours:
            try:
                time_str = hour.get("time", "")
                hour_time = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
                
                # Si la hora del registro es >= ahora, usamos este
                if hour_time >= now:
                    return hour
            except:
                continue
        
        # Fallback: último registro
        return hours[-1] if hours else {}
    
    def _find_current_hour_index(self, hours: list) -> int:
        """Encuentra el índice del registro más cercano a la hora actual"""
        now = datetime.now(timezone.utc)
        
        for i, hour in enumerate(hours):
            try:
                time_str = hour.get("time", "")
                hour_time = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
                
                if hour_time >= now:
                    return i
            except:
                continue
        
        return 0
    
    def _extract_weather_data(self, hour_data: dict, tide_state: str) -> WeatherData:
        """Extrae WeatherData de un registro horario de Stormglass"""
        
        # Stormglass retorna datos de múltiples fuentes, usamos "sg" (Stormglass)
        # El formato es: {"windSpeed": {"sg": 5.2, "noaa": 4.8}}
        
        def get_value(param: str) -> Optional[float]:
            """Obtiene valor de un parámetro, prefiriendo fuente 'sg'"""
            param_data = hour_data.get(param, {})
            if isinstance(param_data, dict):
                return param_data.get("sg") or param_data.get("noaa") or param_data.get("icon")
            return param_data
        
        wind_speed_ms = get_value("windSpeed")  # Viene en m/s
        wind_direction = get_value("windDirection")
        wave_height = get_value("waveHeight")
        
        # Convertir wind speed de m/s a km/h
        wind_speed_kmh = wind_speed_ms * 3.6 if wind_speed_ms else None
        
        timestamp = hour_data.get("time", datetime.now(timezone.utc).isoformat())
        
        return WeatherData(
            wind=WindData(
                speed_kmh=round(wind_speed_kmh, 1) if wind_speed_kmh else None,
                direction_deg=int(wind_direction) if wind_direction else None,
                relative_direction=None
            ),
            waves=WaveData(
                height_m=round(wave_height, 2) if wave_height else None
            ),
            tide=TideData(state=tide_state),
            timestamp=timestamp,
            provider="stormglass"
        )
    
    async def _get_tide_state(self, lat: float, lon: float) -> str:
        """Obtiene estado de marea del provider configurado"""
        if self.tide_provider:
            try:
                return await self.tide_provider.get_tide_state(lat, lon)
            except Exception as e:
                logger.error(f"Tide provider error: {e}")
        return "rising"
