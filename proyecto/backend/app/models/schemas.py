from pydantic import BaseModel, Field
from typing import Optional, List, Literal

# ==================== User Profile ====================

class UserProfile(BaseModel):
    board_type: Literal["rigid", "inflable"] = Field(..., description="Tipo de tabla")
    experience: Literal["beginner", "intermediate", "advanced"] = Field(..., description="Nivel de experiencia")
    paddle_power: Literal["low", "medium", "high"] = Field(..., description="Potencia de remada")
    session_goal: Literal["calma", "entrenamiento", "desafio"] = Field(default="calma", description="Objetivo de la sesión")

# ==================== Weather Data ====================

class WindData(BaseModel):
    speed_kmh: Optional[float] = Field(None, description="Velocidad del viento en km/h")
    direction_deg: Optional[int] = Field(None, ge=0, le=360, description="Dirección del viento en grados (0=Norte)")
    relative_direction: Optional[str] = Field(None, description="Dirección relativa: onshore/offshore/cross")

class WaveData(BaseModel):
    height_m: Optional[float] = Field(None, ge=0, description="Altura de olas en metros")
    period_s: Optional[float] = Field(None, ge=0, description="Periodo de olas en segundos")
    direction_deg: Optional[int] = Field(None, ge=0, le=360, description="Dirección de olas en grados")

class AtmosphereData(BaseModel):
    temperature_c: Optional[float] = Field(None, description="Temperatura ambiente en °C")
    precipitation_mm: Optional[float] = Field(None, ge=0, description="Precipitación en mm")
    cloud_cover_pct: Optional[int] = Field(None, ge=0, le=100, description="Cobertura de nubes %")
    uv_index: Optional[float] = Field(None, ge=0, description="Índice UV máximo")
    visibility_km: Optional[float] = Field(None, ge=0, description="Visibilidad en km")
    weather_code: Optional[int] = Field(None, description="Código WMO de clima")

class TideData(BaseModel):
    state: Literal["rising", "falling", "high", "low"] = Field(..., description="Estado de la marea")

class WeatherData(BaseModel):
    wind: WindData
    waves: WaveData
    atmosphere: Optional[AtmosphereData] = None
    tide: TideData
    timestamp: str = Field(..., description="Timestamp de los datos")
    provider: str = Field(default="openmeteo", description="Proveedor de datos")

# ==================== Engine Results ====================

class Scores(BaseModel):
    seguridad: int = Field(..., ge=0, le=100, description="Score de seguridad (0-100, alto=seguro)")
    esfuerzo: int = Field(..., ge=0, le=100, description="Score de esfuerzo (0-100)")
    disfrute: int = Field(..., ge=0, le=100, description="Score de disfrute (0-100)")

class Categories(BaseModel):
    seguridad: Literal["bajo", "medio", "alto"] = Field(..., description="Categoría de seguridad")
    esfuerzo: Literal["bajo", "medio", "alto"] = Field(..., description="Categoría de esfuerzo")
    disfrute: Literal["bajo", "medio", "alto"] = Field(..., description="Categoría de disfrute")

class ConfidenceFactors(BaseModel):
    data_completeness: float = Field(..., description="Completitud de datos (0-1)")
    data_freshness: float = Field(..., description="Frescura de datos (0-1)")
    volatility: float = Field(..., description="Volatilidad detectada (0-1)")

class SemanticAnalysis(BaseModel):
    """Modelo fenomenológico HAX v6: Micro-narrativas + personalización + cierre pedagógico"""
    scenario_id: str = Field(..., description="ID del escenario clasificado")
    driver_desc: str = Field(..., description="Qué está moviendo el agua")
    behavior_desc: str = Field(..., description="Cómo se ve la superficie")
    body_desc: str = Field(..., description="Qué vas a sentir en el cuerpo")
    risk_desc: str = Field(..., description="El riesgo de hoy y por qué")
    avoid_desc: str = Field(..., description="Qué NO hacer hoy")
    visual_cues: List[str] = Field(default_factory=list, description="Qué buscar con los ojos")
    strategy_desc: str = Field(..., description="Tu plan para hoy")
    beginner_tip: str = Field(..., description="Consejo para principiantes")
    advanced_tip: str = Field(..., description="Consejo para avanzados")
    learning_focus: str = Field(..., description="Cierre pedagógico - qué practicás hoy")

class EngineResult(BaseModel):
    scores: Scores
    categories: Categories
    flags: List[str] = Field(default_factory=list, description="Flags de alerta")
    semantics: SemanticAnalysis = Field(..., description="Análisis semántico para pedagogía")
    confidence: Literal["alta", "media", "baja"] = Field(..., description="Confianza del modelo")
    confidence_factors: Optional[ConfidenceFactors] = None

# ==================== API Requests/Responses ====================

class AnalyzeRequest(BaseModel):
    spot_id: str = Field(..., description="ID del spot (e.g., 'varese')")
    user: UserProfile

class AnalyzeResponse(BaseModel):
    spot: dict
    weather: WeatherData
    result: EngineResult

class ExplanationRequest(BaseModel):
    user: UserProfile
    weather: WeatherData
    result: EngineResult

class ExplanationResponse(BaseModel):
    explanation: str = Field(..., description="Explicación educativa en markdown")
    glossary_terms: List[str] = Field(default_factory=list, description="Términos del glosario mencionados")

class NearestSpotResponse(BaseModel):
    spot_id: str
    name: str
    distance_km: float

# ==================== Timeline ====================

class TimelinePoint(BaseModel):
    timestamp: str = Field(..., description="Timestamp ISO")
    hour_label: str = Field(..., description="Etiqueta hora (ej: 14:00)")
    result: EngineResult = Field(..., description="Resultado del motor para esta hora")
    weather: WeatherData = Field(..., description="Datos climáticos para esta hora")

class TimelineResponse(BaseModel):
    spot: dict
    weather: WeatherData
    current: EngineResult
    timeline: List[TimelinePoint] = Field(..., description="Proyección horaria")

class TimelineRequest(BaseModel):
    spot_id: str
    user: UserProfile
