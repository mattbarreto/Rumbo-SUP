"""
Weather Provider - OpenMeteo Only
Prioriza datos REALES para deportistas de SUP.
Caché agresivo para evitar rate limits.
"""

import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, List, Tuple
from app.services.weather_service import WeatherProvider
from app.models.schemas import WeatherData
import logging

logger = logging.getLogger(__name__)

# Cache global (en memoria) - 15 minutos es suficiente para datos meteorológicos
_weather_cache: Dict[str, Tuple[datetime, WeatherData]] = {}
_forecast_cache: Dict[str, Tuple[datetime, List[WeatherData]]] = {}

CACHE_TTL_MINUTES = 15  # Datos frescos (OpenMeteo actualiza cada hora)


class HybridWeatherProvider(WeatherProvider):
    """
    Provider simplificado - SOLO OpenMeteo.
    Datos reales y precisos para deportistas de SUP.
    """
    
    def __init__(self, stormglass_provider=None, openweather_provider=None, openmeteo_provider=None, windy_provider=None, tide_provider=None):
        # Solo usamos OpenMeteo - los demás están para compatibilidad pero no se usan
        self.openmeteo = openmeteo_provider
        self.tide_provider = tide_provider
        
        if not self.openmeteo:
            logger.error("❌ CRÍTICO: OpenMeteo provider no configurado!")
    
    def _get_cache_key(self, lat: float, lon: float) -> str:
        """Genera key de caché redondeando coordenadas"""
        return f"{round(lat, 2)},{round(lon, 2)}"
    
    def _is_cache_valid(self, cached_time: datetime) -> bool:
        """Verifica si el caché está fresco (15 min)"""
        now = datetime.now(timezone.utc)
        age = now - cached_time
        return age < timedelta(minutes=CACHE_TTL_MINUTES)

    async def get_conditions(self, lat: float, lon: float) -> WeatherData:
        """Obtiene condiciones actuales - SOLO OpenMeteo con caché"""
        cache_key = self._get_cache_key(lat, lon)
        
        # 1. Revisar caché PRIMERO (evita llamadas innecesarias)
        if cache_key in _weather_cache:
            cached_time, cached_data = _weather_cache[cache_key]
            if self._is_cache_valid(cached_time):
                age_sec = int((datetime.now(timezone.utc) - cached_time).total_seconds())
                logger.info(f"📦 Cache HIT - datos de hace {age_sec}s")
                return cached_data
        
        # 2. Llamar a OpenMeteo (única fuente)
        if not self.openmeteo:
            raise ValueError("OpenMeteo provider no configurado")
        
        try:
            logger.info("🌐 Llamando a OpenMeteo API...")
            data = await self.openmeteo.get_conditions(lat, lon)
            
            # Validar que recibimos datos reales
            if data.wind.speed_kmh is None:
                logger.error("❌ OpenMeteo retornó datos vacíos de viento")
                raise ValueError("OpenMeteo no retornó datos de viento")
            
            # Guardar en caché
            _weather_cache[cache_key] = (datetime.now(timezone.utc), data)
            logger.info(f"✅ OpenMeteo: Viento {data.wind.speed_kmh:.1f} km/h, Olas {data.waves.height_m:.2f}m")
            return data
            
        except Exception as e:
            logger.error(f"❌ OpenMeteo falló: {e}")
            
            # Si hay caché viejo, usarlo como emergencia
            if cache_key in _weather_cache:
                cached_time, cached_data = _weather_cache[cache_key]
                age_min = int((datetime.now(timezone.utc) - cached_time).total_seconds() / 60)
                logger.warning(f"⚠️ Usando caché de emergencia (edad: {age_min} min)")
                return cached_data
            
            raise ValueError(f"OpenMeteo no disponible y no hay caché: {e}")
    
    async def get_forecast(self, lat: float, lon: float, hours: int = 12) -> List[WeatherData]:
        """Obtiene forecast - SOLO OpenMeteo con caché"""
        cache_key = f"{self._get_cache_key(lat, lon)}_forecast"
        
        # 1. Revisar caché PRIMERO
        if cache_key in _forecast_cache:
            cached_time, cached_data = _forecast_cache[cache_key]
            if self._is_cache_valid(cached_time):
                age_sec = int((datetime.now(timezone.utc) - cached_time).total_seconds())
                logger.info(f"📦 Forecast cache HIT - datos de hace {age_sec}s")
                return cached_data[:hours]
        
        # 2. Llamar a OpenMeteo (única fuente)
        if not self.openmeteo:
            raise ValueError("OpenMeteo provider no configurado")
        
        try:
            logger.info("🌐 Llamando a OpenMeteo API (forecast)...")
            data = await self.openmeteo.get_forecast(lat, lon, hours)
            
            if not data:
                raise ValueError("OpenMeteo no retornó datos de forecast")
            
            # Guardar en caché
            _forecast_cache[cache_key] = (datetime.now(timezone.utc), data)
            logger.info(f"✅ OpenMeteo forecast: {len(data)} horas de datos")
            return data
            
        except Exception as e:
            logger.error(f"❌ OpenMeteo forecast falló: {e}")
            
            # Usar caché viejo como emergencia
            if cache_key in _forecast_cache:
                cached_time, cached_data = _forecast_cache[cache_key]
                age_min = int((datetime.now(timezone.utc) - cached_time).total_seconds() / 60)
                logger.warning(f"⚠️ Usando forecast en caché de emergencia (edad: {age_min} min)")
                return cached_data[:hours]
            
            raise ValueError(f"OpenMeteo forecast no disponible y no hay caché: {e}")


def clear_cache():
    """Limpia caché (útil para testing)"""
    global _weather_cache, _forecast_cache
    _weather_cache = {}
    _forecast_cache = {}
    logger.info("🧹 Cache limpiado")

