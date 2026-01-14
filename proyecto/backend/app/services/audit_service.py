
import httpx
import asyncio
import logging
import os
from datetime import datetime
from app.config.spots import SPOTS

logger = logging.getLogger(__name__)

class AuditService:
    """
    Servicio de Auditoría Forense para Proveedores de Clima via HTTPX.
    Prueba conectividad, latencia y completitud de datos desde el entorno de producción.
    """

    def __init__(self):
        self.headers = {"User-Agent": "RumboSUP-Audit/1.0"}
        # Varese como spot de control
        self.lat = SPOTS["varese"]["lat"]
        self.lon = SPOTS["varese"]["lon"]

    async def _timed_request(self, url, params=None, method="GET", json_body=None):
        start = datetime.now()
        status = "UNKNOWN"
        code = 0
        data_preview = None
        error_msg = None
        
        try:
            async with httpx.AsyncClient(timeout=10.0, headers=self.headers) as client:
                if method == "GET":
                    res = await client.get(url, params=params)
                else:
                    res = await client.post(url, json=json_body)
                
                code = res.status_code
                latency_ms = (datetime.now() - start).total_seconds() * 1000
                
                if res.is_success:
                    status = "OK"
                    try:
                        data_preview = res.json()
                    except:
                        data_preview = "Not JSON"
                else:
                    status = "FAIL"
                    error_msg = res.text[:200]  # First 200 chars

                return {
                    "status": status,
                    "code": code,
                    "latency_ms": round(latency_ms, 2),
                    "error": error_msg,
                    "data_preview": str(data_preview)[:100] + "..." if data_preview else None
                }
        except Exception as e:
            latency_ms = (datetime.now() - start).total_seconds() * 1000
            return {
                "status": "ERROR",
                "code": 0,
                "latency_ms": round(latency_ms, 2),
                "error": str(e)
            }

    async def check_openmeteo(self):
        """Test OpenMeteo Forecast & Marine"""
        # 1. Forecast (Wind)
        forecast_url = "https://api.open-meteo.com/v1/forecast"
        forecast_params = {
            "latitude": self.lat, "longitude": self.lon,
            "hourly": "wind_speed_10m",
            "forecast_days": 1
        }
        res_forecast = await self._timed_request(forecast_url, forecast_params)

        # 2. Marine (Waves)
        marine_url = "https://marine-api.open-meteo.com/v1/marine"
        marine_params = {
            "latitude": self.lat, "longitude": self.lon,
            "hourly": "wave_height",
            "forecast_days": 1
        }
        res_marine = await self._timed_request(marine_url, marine_params)

        return {
            "forecast_api": res_forecast,
            "marine_api": res_marine,
            "overall": "OK" if res_forecast["status"] == "OK" and res_marine["status"] == "OK" else "DEGRADED"
        }

    async def check_openweather(self):
        """Test OpenWeather Map"""
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return {"status": "SKIPPED", "error": "No API Key configured"}

        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"lat": self.lat, "lon": self.lon, "appid": api_key}
        
        return await self._timed_request(url, params)

    async def check_windy(self):
        """Test Windy Stability/Reachability"""
        # Usamos una key dummy si no hay, solo para probar conectividad (esperamos 401 si conecta, timeout si bloqueado)
        api_key = os.getenv("WINDY_API_KEY", "dummy_verification_key")
        
        url = "https://api.windy.com/api/point-forecast/v2"
        payload = {
            "lat": self.lat,
            "lon": self.lon,
            "model": "gfs",
            "parameters": ["wind", "waves_height"],
            "levels": ["surface"],
            "key": api_key
        }
        
        res = await self._timed_request(url, method="POST", json_body=payload)
        
        # Interpretación
        if res["code"] == 200:
            conclusion = "READY TO GO (Valid Key)"
        elif res["code"] == 401: # Unauthorized
            conclusion = "REACHABLE (Invalid/Missing Key) - Network OK"
        elif res["status"] == "ERROR":
            conclusion = "UNREACHABLE (Network/Block)"
        else:
            conclusion = f"UNEXPECTED ({res['code']})"
            
        res["conclusion"] = conclusion
        return res

    async def run_audit(self):
        """Run all checks parallel"""
        om, ow, windy = await asyncio.gather(
            self.check_openmeteo(),
            self.check_openweather(),
            self.check_windy()
        )
        
        return {
            "timestamp": datetime.now().isoformat(),
            "environment_check": {
                "VITE_API_URL_set": bool(os.getenv("VITE_API_URL")),
                "OPENWEATHER_KEY_set": bool(os.getenv("OPENWEATHER_API_KEY")),
                "WINDY_KEY_set": bool(os.getenv("WINDY_API_KEY"))
            },
            "providers": {
                "openmeteo": om,
                "openweather": ow,
                "windy": windy
            }
        }
