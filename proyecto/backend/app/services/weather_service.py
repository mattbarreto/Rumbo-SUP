from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
from app.models.schemas import WeatherData, WindData, WaveData, TideData

class WeatherProvider(ABC):
    """
    Interface base para proveedores de datos meteorológicos
    Permite cambiar providers sin tocar la lógica del motor
    """
    
    @abstractmethod
    async def get_conditions(self, lat: float, lon: float) -> WeatherData:
        """
        Obtiene condiciones meteorológicas actuales
        
        Args:
            lat: Latitud
            lon: Longitud
            
        Returns:
            WeatherData normalizado
        """
        pass

class WeatherService:
    """
    Servicio de clima con inyección de dependencia
    Usa el provider configurado para obtener datos
    """
    
    def __init__(self, provider: WeatherProvider):
        self.provider = provider
    
    async def get_current_conditions(self, lat: float, lon: float) -> WeatherData:
        """
        Obtiene condiciones actuales usando el provider configurado
        """
        return await self.provider.get_conditions(lat, lon)
