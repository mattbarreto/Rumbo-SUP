"""
Hybrid Weather Provider with Caching

Combina múltiples providers con:
1. Caché en memoria (30 min)
2. Stormglass como primario (más confiable)
3. OpenMeteo como fallback
"""

import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, List, Tuple
from app.services.weather_service import WeatherProvider
from app.models.schemas import WeatherData
import logging

logger = logging.getLogger(__name__)

# Cache global simple (en memoria)
# Key: "lat,lon" -> Value: (timestamp, WeatherData)
_weather_cache: Dict[str, Tuple[datetime, WeatherData]] = {}
_forecast_cache: Dict[str, Tuple[datetime, List[WeatherData]]] = {}
CACHE_TTL_MINUTES = 30


class HybridWeatherProvider(WeatherProvider):
    """
    Provider híbrido que:
    1. Revisa caché primero
    2. Intenta Stormglass (si hay API key)
    3. Fallback a OpenMeteo
    4. Cachea resultados
    """
    
    def __init__(self, stormglass_provider=None, openweather_provider=None, openmeteo_provider=None, tide_provider=None):
        self.stormglass = stormglass_provider
        self.openweather = openweather_provider
        self.openmeteo = openmeteo_provider
        self.tide_provider = tide_provider
    
    def _get_cache_key(self, lat: float, lon: float) -> str:
        """Genera key de caché redondeando coordenadas"""
        return f"{round(lat, 2)},{round(lon, 2)}"
    
    def _is_cache_valid(self, cached_time: datetime) -> bool:
        """Verifica si el caché aún es válido"""
        now = datetime.now(timezone.utc)
        return (now - cached_time) < timedelta(minutes=CACHE_TTL_MINUTES)
    
    async def get_conditions(self, lat: float, lon: float) -> WeatherData:
        """Obtiene condiciones con caché y fallback"""
        cache_key = self._get_cache_key(lat, lon)
        
        # 1. Revisar caché
        if cache_key in _weather_cache:
            cached_time, cached_data = _weather_cache[cache_key]
            if self._is_cache_valid(cached_time):
                logger.info(f"📦 Cache hit for {cache_key}")
                return cached_data
        
        # 2. Intentar Stormglass primero
        if self.stormglass:
            try:
                data = await self.stormglass.get_conditions(lat, lon)
                _weather_cache[cache_key] = (datetime.now(timezone.utc), data)
                logger.info("✅ Stormglass success, cached")
                return data
            except Exception as e:
                logger.warning(f"⚠️ Stormglass failed: {e}, trying OpenWeather...")
        
        # 3. Intentar OpenWeather
        if self.openweather:
            try:
                data = await self.openweather.get_conditions(lat, lon)
                _weather_cache[cache_key] = (datetime.now(timezone.utc), data)
                logger.info("✅ OpenWeather success, cached")
                return data
            except Exception as e:
                logger.warning(f"⚠️ OpenWeather failed: {e}, trying OpenMeteo...")
        
        # 3. Fallback a OpenMeteo
        if self.openmeteo:
            try:
                data = await self.openmeteo.get_conditions(lat, lon)
                _weather_cache[cache_key] = (datetime.now(timezone.utc), data)
                logger.info("✅ OpenMeteo success, cached")
                return data
            except Exception as e:
                logger.error(f"❌ OpenMeteo also failed: {e}")
                raise
        
        raise ValueError("No weather providers available")
    
    async def get_forecast(self, lat: float, lon: float, hours: int = 12) -> List[WeatherData]:
        """Obtiene forecast con caché y fallback"""
        cache_key = f"{self._get_cache_key(lat, lon)}_forecast"
        
        # 1. Revisar caché
        if cache_key in _forecast_cache:
            cached_time, cached_data = _forecast_cache[cache_key]
            if self._is_cache_valid(cached_time):
                logger.info(f"📦 Forecast cache hit for {cache_key}")
                return cached_data[:hours]
        
        # 2. Intentar Stormglass primero
        if self.stormglass:
            try:
                data = await self.stormglass.get_forecast(lat, lon, hours)
                if data:
                    _forecast_cache[cache_key] = (datetime.now(timezone.utc), data)
                    logger.info("✅ Stormglass forecast success, cached")
                    return data
            except Exception as e:
                logger.warning(f"⚠️ Stormglass forecast failed: {e}, trying OpenWeather...")
        
        # 3. Intentar OpenWeather
        if self.openweather:
            try:
                data = await self.openweather.get_forecast(lat, lon, hours)
                if data:
                    _forecast_cache[cache_key] = (datetime.now(timezone.utc), data)
                    logger.info("✅ OpenWeather forecast success, cached")
                    return data
            except Exception as e:
                logger.warning(f"⚠️ OpenWeather forecast failed: {e}, trying OpenMeteo...")
        
        # 3. Fallback a OpenMeteo
        if self.openmeteo:
            try:
                data = await self.openmeteo.get_forecast(lat, lon, hours)
                if data:
                    _forecast_cache[cache_key] = (datetime.now(timezone.utc), data)
                    logger.info("✅ OpenMeteo forecast success, cached")
                    return data
            except Exception as e:
                logger.error(f"❌ OpenMeteo forecast also failed: {e}")
                raise
        
        raise ValueError("No weather providers available for forecast")


def clear_cache():
    """Limpia caché (útil para testing)"""
    global _weather_cache, _forecast_cache
    _weather_cache = {}
    _forecast_cache = {}
    logger.info("🧹 Weather cache cleared")
