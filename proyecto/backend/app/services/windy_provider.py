
import httpx
import asyncio
import os
import math
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.services.weather_service import WeatherProvider
from app.models.schemas import WeatherData, WindData, WaveData, AtmosphereData, TideData

logger = logging.getLogger(__name__)

class WindyProvider(WeatherProvider):
    """
    Proveedor para Windy.com Point Forecast API v2.
    Usa modelo GFS (Global) para Viento/Clima y GFS-Wave para Olas.
    """
    
    API_URL = "https://api.windy.com/api/point-forecast/v2"
    
    def __init__(self, api_key: str = None, tide_provider: Any = None):
        self.api_key = api_key or os.getenv("WINDY_API_KEY")
        self.tide_provider = tide_provider

    async def get_conditions(self, lat: float, lon: float) -> WeatherData:
        """Obtiene condiciones actuales usando Windy (GFS + GFS-Wave)"""
        
        if not self.api_key:
            raise ValueError("WINDY_API_KEY no configurada")

        # 1. Fetch de ambos modelos en paralelo
        gfs_payload = {
            "lat": lat, "lon": lon, 
            "model": "gfs", 
            "parameters": ["wind", "temp", "precip", "clouds"], 
            "levels": ["surface"], 
            "key": self.api_key
        }
        
        wave_payload = {
            "lat": lat, "lon": lon, 
            "model": "gfsWave", 
            "parameters": ["waves", "windWaves", "swell1"], 
            "levels": ["surface"], 
            "key": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            resp_gfs, resp_wave = await asyncio.gather(
                client.post(self.API_URL, json=gfs_payload),
                client.post(self.API_URL, json=wave_payload)
            )

        if resp_gfs.status_code != 200 or resp_wave.status_code != 200:
            error_msg = f"Windy Error. GFS: {resp_gfs.status_code}, Wave: {resp_wave.status_code}"
            logger.error(error_msg)
            # Intentar leer el body del error para más detalle
            logger.error(f"GFS Body: {resp_gfs.text[:200]}")
            logger.error(f"Wave Body: {resp_wave.text[:200]}")
            raise ValueError(error_msg)

        data_gfs = resp_gfs.json()
        data_wave = resp_wave.json()

        # 2. Extraer índices actuales (Windy devuelve arrays de tiempo UNIX)
        # Buscamos el timestamp más cercano al "ahora"
        # Windy timestamps son ms desde epoch
        now_ms = datetime.now().timestamp() * 1000
        
        # Helper para encontrar index
        def get_current_index(ts_array):
            if not ts_array: return -1
            # Busca el primer tiempo que sea mayor o igual a ahora (o el último si ya pasó)
            # Como son forecast, "ahora" debería estar cerca del principio
            closest_idx = 0
            min_diff = float('inf')
            
            for i, ts in enumerate(ts_array):
                diff = abs(ts - now_ms)
                if diff < min_diff:
                    min_diff = diff
                    closest_idx = i
            return closest_idx

        idx_gfs = get_current_index(data_gfs.get("ts", []))
        idx_wave = get_current_index(data_wave.get("ts", []))

        if idx_gfs == -1 or idx_wave == -1:
            raise ValueError("Windy no devolvió serie de tiempo válida")

        # 3. Mapear Datos GFS (Viento vector -> Scalar)
        # wind_u-surface, wind_v-surface
        u = data_gfs.get("wind_u-surface", [])[idx_gfs]
        v = data_gfs.get("wind_v-surface", [])[idx_gfs]
        
        # Convertir U/V a Speed/Dir
        # Speed = sqrt(u^2 + v^2)
        # Dir = atan2(u, v) ... Nota: Metereological direction is where wind comes FROM.
        # Standard math atan2(y, x) -> Cartesian angle.
        # Wind U (Zonal) : West -> East (+).
        # Wind V (Meridional): South -> North (+).
        # Math Direction (from East counter-clockwise): atan2(v, u).
        # Met Direction (0=N, 90=E, 180=S, 270=W): 
        #   Deg = (270 - atan2(v, u) * 180 / PI) % 360
        
        speed_ms = math.sqrt(u*u + v*v) if (u is not None and v is not None) else 0
        speed_kmh = speed_ms * 3.6
        
        direction_deg = 0
        if u is not None and v is not None:
            angle_rad = math.atan2(v, u)
            angle_deg = math.degrees(angle_rad)
            # Convert mth angle to meteorological azimuth (N=0, E=90)
            # From: http://cola.gmu.edu/bb/data/grads/gadoc/gadoc.php?file=scriptmath
            # dir = 180 + (180/pi)*atan2(u,v) ? No, that's flow direction. 
            # Standard conversion:
            direction_deg = (180 + math.degrees(math.atan2(u, v))) % 360 # Flow Direction
            # But we want SOURCE direction. So +180 to flip it?
            # Actually simplest: Met Dir = 270 - MathDir.
            # Let's use a safe standard formula.
            direction_deg = (270 - math.degrees(math.atan2(v, u))) % 360

        # 4. Mapear Datos Wave
        # waves_height-surface
        wave_h = data_wave.get("waves_height-surface", [])[idx_wave]
        wave_p = data_wave.get("waves_period-surface", [])[idx_wave]
        wave_d = data_wave.get("waves_direction-surface", [])[idx_wave]

        # 5. Marea (Usar Provider Externo inyectado o N/A)
        # Windy no tiene tides.
        tide_data = TideData(state="high") # Default safe
        if self.tide_provider:
            try:
                tide_data = await self.tide_provider.get_tide_data(lat, lon, datetime.now())
            except Exception as e:
                logger.warning(f"Tide provider failed in Windy: {e}")

        # 6. Construir WeatherData
        return WeatherData(
            wind=WindData(
                speed_kmh=speed_kmh,
                direction_deg=direction_deg,
                relative_direction=None 
            ),
            waves=WaveData(
                height_m=wave_h,
                period_s=wave_p,
                direction_deg=wave_d
            ),
            atmosphere=AtmosphereData(
                temperature_c=data_gfs.get("temp-surface", [])[idx_gfs] - 273.15, # Kelvin to C
                precipitation_mm=data_gfs.get("past3hprecip-surface", [])[idx_gfs],
                cloud_cover_pct=None, # TBD logic for lclouds/mclouds
                uv_index=None,
                visibility_km=None,
                weather_code=None
            ),
            tide=tide_data,
            timestamp=datetime.now().isoformat(),
            provider="windy_gfs"
        )

    async def get_forecast(self, lat: float, lon: float, hours: int = 12) -> List[WeatherData]:
        return [] # Implementar luego si se requiere timeline completo
