from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest, AnalyzeResponse, ExplanationRequest, ExplanationResponse, NearestSpotResponse, TimelineRequest, TimelineResponse, TimelinePoint
from app.config.spots import SPOTS
from datetime import datetime
from tenacity import RetryError
from httpx import ConnectTimeout, ReadTimeout
import math
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["api"])

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_conditions(request: AnalyzeRequest):
    """
    Analiza condiciones para un spot y usuario
    Usa datos reales de OpenMeteo + Motor determinístico
    """
    # Validar spot existe
    if request.spot_id not in SPOTS:
        raise HTTPException(status_code=404, detail=f"Spot '{request.spot_id}' no encontrado")
    
    spot = SPOTS[request.spot_id]
    
    try:
        # Obtener datos meteorológicos REALES de OpenMeteo
        from app.services.openmeteo_provider import OpenMeteoProvider
        from app.services.weather_service import WeatherService
        from app.services.noaa_tides_provider import NOAATidesProvider
        import os
        
        # Configurar providers - NOAA es GRATIS, no requiere API key
        noaa_tides = NOAATidesProvider()
        
        openmeteo_provider = OpenMeteoProvider(tide_provider=noaa_tides)
        weather_service = WeatherService(openmeteo_provider)
        
        weather_data = await weather_service.get_current_conditions(
            spot["lat"], 
            spot["lon"]
        )
        
        # Ejecutar motor determinístico (Layer A)
        from app.services.sensei_engine import SenseiEngine
        engine = SenseiEngine()
        result = engine.analyze(weather_data, request.spot_id, request.user)
        
        return AnalyzeResponse(
            spot={"name": spot["name"], "lat": spot["lat"], "lon": spot["lon"]},
            weather=weather_data,
            result=result
        )
    except ValueError as e:
        logger.error(f"Error validating data: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except (RetryError, ConnectTimeout, ReadTimeout) as e:
        logger.error(f"Upstream API error: {e}")
        raise HTTPException(status_code=503, detail="Weather service unavailable (upstream timeout)")
    except Exception as e:
        logger.error(f"Error in analyze_conditions: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/pedagogy/explain", response_model=ExplanationResponse)
async def explain_conditions(request: ExplanationRequest):
    """
    Genera explicación pedagógica usando Gemini (Layer B)
    Solo explica, NUNCA decide
    """
    from app.services.pedagogy_service import PedagogyService
    
    pedagogy = PedagogyService()
    explanation = await pedagogy.generate_explanation(
        request.user,
        request.weather,
        request.result
    )
    
    return ExplanationResponse(
        explanation=explanation,
        glossary_terms=[]  # TODO: Fase futura - extraer términos del glosario
    )

@router.get("/spots/nearest", response_model=NearestSpotResponse)
async def get_nearest_spot(lat: float, lon: float):
    """
    Retorna el spot más cercano a las coordenadas dadas
    """
    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calcula distancia en km usando fórmula haversine"""
        R = 6371  # Radio de la Tierra en km
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    # Calcular distancia a todos los spots
    nearest = None
    min_distance = float('inf')
    
    for spot_id, spot_data in SPOTS.items():
        distance = haversine_distance(lat, lon, spot_data["lat"], spot_data["lon"])
        if distance < min_distance:
            min_distance = distance
            nearest = {
                "spot_id": spot_id,
                "name": spot_data["name"],
                "distance_km": round(distance, 2)
            }
    
    if not nearest:
        raise ValueError("No se encontraron spots cercanos")
    
    return NearestSpotResponse(**nearest)

@router.post("/timeline", response_model=TimelineResponse)
async def get_timeline(request: TimelineRequest):
    """
    Obtiene línea de tiempo semántica (forecast + engine)
    """
    from app.models.schemas import TimelineResponse, TimelinePoint
    
    if request.spot_id not in SPOTS:
        raise HTTPException(status_code=404, detail=f"Spot '{request.spot_id}' no encontrado")
    
    spot = SPOTS[request.spot_id]
    
    try:
        # Setup services (inline)
        from app.services.openmeteo_provider import OpenMeteoProvider
        from app.services.weather_service import WeatherService
        from app.services.noaa_tides_provider import NOAATidesProvider
        from app.services.sensei_engine import SenseiEngine
        import os
        
        # Configurar providers - NOAA es GRATIS
        noaa_tides = NOAATidesProvider()
        
        openmeteo_provider = OpenMeteoProvider(tide_provider=noaa_tides)
        weather_service = WeatherService(openmeteo_provider)
        engine = SenseiEngine()
        
        # Obtener forecast 12hs
        forecast = await weather_service.get_forecast(spot["lat"], spot["lon"], hours=12)
        
        timeline_points = []
        
        for wd in forecast:
            # Ejecutar engine para cada hora
            result = engine.analyze(wd, request.spot_id, request.user)
            
            # Formatear hora
            try:
                ts = datetime.fromisoformat(wd.timestamp)
                label = ts.strftime("%H:%M")
            except:
                label = "--:--"
                
            timeline_points.append(TimelinePoint(
                timestamp=wd.timestamp,
                hour_label=label,
                result=result,
                weather=wd
            ))
            
        if not timeline_points:
            raise ValueError("No se pudieron obtener datos de pronóstico")
            
        return TimelineResponse(
            spot={"name": spot["name"], "lat": spot["lat"], "lon": spot["lon"]},
            weather=forecast[0], # El primero es el actual
            current=timeline_points[0].result,
            timeline=timeline_points
        )
    except ValueError as e:
        logger.error(f"Error fetching timeline data: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except (RetryError, ConnectTimeout, ReadTimeout) as e:
        logger.error(f"Upstream API error: {e}")
        raise HTTPException(status_code=503, detail="Weather service unavailable (upstream timeout)")
    except Exception as e:
        logger.error(f"Error in get_timeline: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
