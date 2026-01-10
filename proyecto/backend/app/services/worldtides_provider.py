import httpx
from datetime import datetime, timezone, timedelta
from typing import Optional

class WorldTidesProvider:
    """
    Provider para datos de marea usando WorldTides API
    Gratis: 100 requests/mes
    Docs: https://www.worldtides.info/apidocs
    """
    
    BASE_URL = "https://www.worldtides.info/api/v3"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def get_tide_state(self, lat: float, lon: float) -> str:
        """
        Obtiene estado actual de la marea (rising/falling/high/low)
        
        Returns:
            "rising", "falling", "high", "low"
        """
        try:
            # Obtener extremos de marea (high/low tides) para hoy
            params = {
                "extremes": "",  # Obtener extremos (high/low)
                "lat": lat,
                "lon": lon,
                "key": self.api_key,
                "days": 1  # Solo hoy
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(self.BASE_URL, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
            
            if "extremes" not in data:
                return "rising"  # Fallback
            
            extremes = data["extremes"]
            now = datetime.now(timezone.utc)
            
            # Encontrar extremos más cercanos (anterior y siguiente)
            past_extremes = [e for e in extremes if datetime.fromtimestamp(e["dt"], tz=timezone.utc) <= now]
            future_extremes = [e for e in extremes if datetime.fromtimestamp(e["dt"], tz=timezone.utc) > now]
            
            if not past_extremes or not future_extremes:
                return "rising"  # Fallback
            
            last_extreme = past_extremes[-1]  # Último extremo pasado
            next_extreme = future_extremes[0]  # Próximo extremo
            
            # Determinar estado
            last_was_high = last_extreme["type"] == "High"
            next_is_high = next_extreme["type"] == "High"
            
            # Calcular tiempo transcurrido vs tiempo total entre extremos
            last_time = datetime.fromtimestamp(last_extreme["dt"], tz=timezone.utc)
            next_time = datetime.fromtimestamp(next_extreme["dt"], tz=timezone.utc)
            total_duration = (next_time - last_time).total_seconds()
            elapsed = (now - last_time).total_seconds()
            progress = elapsed / total_duration if total_duration > 0 else 0.5
            
            # Si estamos muy cerca de un extremo (< 5% del ciclo)
            if progress < 0.05:
                return "high" if last_was_high else "low"
            elif progress > 0.95:
                return "high" if next_is_high else "low"
            
            # Estado normal: subiendo o bajando
            if last_was_high:
                return "falling"  # Después de high, está bajando
            else:
                return "rising"  # Después de low, está subiendo
                
        except Exception as e:
            print(f"Error getting tide data from WorldTides: {e}")
            return "rising"  # Fallback seguro
