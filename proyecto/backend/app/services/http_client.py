import httpx
import logging
import asyncio
from typing import Optional, Any, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log

logger = logging.getLogger(__name__)

class ResilientHttpClient:
    """
    Cliente HTTP Singleton y Resiliente
    
    Características:
    - Retries automáticos con Backoff Exponencial
    - Timeouts explícitos
    - Gestión de conexión persistente (Pool)
    - Manejo unificado de errores
    """
    
    _instance = None
    _client: Optional[httpx.AsyncClient] = None
    
    # Configuración de Resiliencia
    MAX_RETRIES = 3
    TIMEOUT_SECONDS = 10.0
    BACKOFF_MIN = 1
    BACKOFF_MAX = 5
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResilientHttpClient, cls).__new__(cls)
        return cls._instance

    @classmethod
    async def get_client(cls) -> httpx.AsyncClient:
        """Obtiene o crea el cliente httpx compartido"""
        if cls._client is None or cls._client.is_closed:
            logger.info("🔌 Inicializando ResilientHttpClient Pool")
            cls._client = httpx.AsyncClient(
                timeout=httpx.Timeout(cls.TIMEOUT_SECONDS, connect=5.0),
                limits=httpx.Limits(max_keepalive_connections=10, max_connections=20),
                headers={"User-Agent": "RumboSUP-Backend/1.0"}
            )
        return cls._client

    @classmethod
    async def close(cls):
        """Cierra el pool de conexiones"""
        if cls._client:
            await cls._client.aclose()
            logger.info("🔌 ResilientHttpClient Pool cerrado")
            cls._client = None
    
    @retry(
        stop=stop_after_attempt(3), # MAX_RETRIES hardcoded for decorator, uses logic below
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.NetworkError, httpx.TimeoutException, httpx.RemoteProtocolError)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    async def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Realiza GET request con política de retry robusta.
        
        Raises:
            httpx.HTTPStatusError: Para errores 4xx/5xx (no reintentados automáticamente si no son transitorios, 
                                  aunque tenacity aquí solo captura Network/Timeout).
            httpx.RequestError: Para errores de red persistentes tras retries.
        """
        client = await self.get_client()
        
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPStatusError as e:
            # Si es 5xx, podríamos querer reintentar. Si es 4xx, probablemente no.
            # Por simplicidad del decorador, aquí dejamos que el caller maneje status errors
            # salvo que extendamos la retry policy.
            
            # Loguear con detalle para observabilidad
            logger.error(f"❌ HTTP Error {e.response.status_code} fetching {url}: {e}")
            raise e
            
        except httpx.RequestError as e:
            logger.warning(f"⚠️ Network Error fetching {url}: {e} - Retrying...")
            raise e  # Tenacity capturará esto
            
        except Exception as e:
            logger.error(f"❌ Unexpected Error fetching {url}: {e}")
            raise e

# Instancia global para uso fácil
http_client = ResilientHttpClient()
