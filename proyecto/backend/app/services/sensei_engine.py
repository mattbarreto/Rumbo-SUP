import math
from typing import List, Tuple
from app.models.schemas import (
    WeatherData, UserProfile, EngineResult, 
    Scores, Categories, ConfidenceFactors
)
from app.config.spots import SPOTS
from datetime import datetime, timezone

class SenseiEngine:
    """
    Motor determinístico (Layer A)
    Calcula seguridad, esfuerzo y disfrute SIN usar IA
    100% reproducible: mismo input → mismo output
    """
    
    def analyze(
        self, 
        weather: WeatherData, 
        spot_id: str, 
        user: UserProfile
    ) -> EngineResult:
        """
        Análisis completo de condiciones
        
        Returns:
            EngineResult con scores, categorías, flags y confianza
        """
        spot = SPOTS.get(spot_id)
        if not spot:
            raise ValueError(f"Spot '{spot_id}' no encontrado")
        
        # Calcular dirección relativa del viento
        wind_relative = self._calculate_wind_relative_direction(
            weather.wind.direction_deg,
            spot["orientation_costa_deg"]
        )
        weather.wind.relative_direction = wind_relative
        
        # Evaluar flags de alerta
        flags = self._evaluate_flags(weather, user, spot)
        
        # Calcular scores
        seguridad = self._calculate_security_score(weather, user, flags)
        esfuerzo = self._calculate_effort_score(weather, user)
        disfrute = self._calculate_enjoyment_score(weather, user, seguridad)
        
        # Categorizar scores
        cat_seguridad = self._categorize_score(seguridad)
        cat_esfuerzo = self._categorize_score(esfuerzo)
        cat_disfrute = self._categorize_score(disfrute)
        
        # Calcular confianza
        confidence, conf_factors = self._calculate_confidence(weather)
        
        # Calcular semántica (Sensei 3.0)
        semantics = self._analyze_semantics(weather, user, flags, spot)
        
        return EngineResult(
            scores=Scores(
                seguridad=seguridad,
                esfuerzo=esfuerzo,
                disfrute=disfrute
            ),
            categories=Categories(
                seguridad=cat_seguridad,
                esfuerzo=cat_esfuerzo,
                disfrute=cat_disfrute
            ),
            flags=flags,
            semantics=semantics,
            confidence=confidence,
            confidence_factors=conf_factors
        )
    
    def _analyze_semantics(
        self,
        weather: WeatherData,
        user: UserProfile,
        flags: List[str],
        spot: dict
    ) -> "SemanticAnalysis":
        """
        HAX v6: Escenario coherente + personalización + cierre pedagógico
        """
        from app.models.schemas import SemanticAnalysis
        from app.services.scenario_catalog import classify_scenario, get_scenario
        
        # 1. Clasificar las condiciones en UN escenario coherente
        scenario_id = classify_scenario(
            wind_speed=weather.wind.speed_kmh,
            wind_rel=weather.wind.relative_direction or "none",
            wave_height=weather.waves.height_m,
            tide_state=weather.tide.state,
            flags=flags
        )
        
        # 2. Obtener el paquete completo de micro-narrativas
        scenario = get_scenario(scenario_id)
        
        # 3. Retornar directamente las frases humanas (no tags)
        return SemanticAnalysis(
            scenario_id=scenario.id,
            driver_desc=scenario.driver_desc,
            behavior_desc=scenario.behavior_desc,
            body_desc=scenario.body_desc,
            risk_desc=scenario.risk_desc,
            avoid_desc=scenario.avoid_desc,
            visual_cues=scenario.visual_cues,
            strategy_desc=scenario.strategy_desc,
            beginner_tip=scenario.beginner_tip,
            advanced_tip=scenario.advanced_tip,
            learning_focus=scenario.learning_focus
        )
    
    def _calculate_wind_relative_direction(
        self, 
        wind_deg: int, 
        coast_deg: int
    ) -> str:
        """
        Calcula dirección relativa del viento respecto a la costa
        
        Returns:
            "onshore" (hacia playa), "offshore" (hacia mar), "cross" (paralelo)
        """
        # Normalizar diferencia angular
        diff = abs(wind_deg - coast_deg)
        if diff > 180:
            diff = 360 - diff
        
        # Clasificar
        if diff < 45:  # Viento en misma dirección que costa mira
            return "offshore"  # Sopla hacia el mar
        elif diff > 135:  # Viento opuesto
            return "onshore"  # Sopla hacia la playa
        else:
            return "cross"  # Viento paralelo a costa
    
    def _evaluate_flags(
        self, 
        weather: WeatherData, 
        user: UserProfile, 
        spot: dict
    ) -> List[str]:
        """
        Evalúa condiciones y retorna flags de alerta
        """
        flags = []
        
        # Flag: Viento fuerte
        if weather.wind.speed_kmh > 30:
            flags.append("viento_fuerte")
        
        # Flag: Riesgo de deriva (offshore + inflable)
        if (weather.wind.relative_direction == "offshore" and 
            user.board_type == "inflable"):
            flags.append("riesgo_deriva")
        
        # Flag: Olas grandes
        if weather.waves.height_m > 1.5:
            flags.append("olas_grandes")
        
        # Flag: Principiante en condiciones moderadas
        if (user.experience == "beginner" and 
            (weather.wind.speed_kmh > 20 or weather.waves.height_m > 1.0)):
            flags.append("principiante_condiciones_moderadas")
        
        # Reglas específicas del spot
        for regla in spot.get("reglas_especificas", []):
            if self._evaluate_spot_rule(regla, weather):
                flags.append(regla["flag"])
        
        return flags
    
    def _evaluate_spot_rule(self, regla: dict, weather: WeatherData) -> bool:
        """
        Evalúa una regla específica del spot
        """
        condition = regla.get("condition", "")
        
        # Regla: marea bajando + viento offshore
        if condition == "tide_falling_and_wind_offshore":
            return (weather.tide.state == "falling" and 
                   weather.wind.relative_direction == "offshore")
        
        return False
    
    def _calculate_security_score(
        self, 
        weather: WeatherData, 
        user: UserProfile, 
        flags: List[str]
    ) -> int:
        """
        Calcula score de SEGURIDAD (0-100, donde 100 = muy seguro)
        ⚠️ NO "riesgo" - el score está invertido
        """
        score = 100  # Empezamos en máxima seguridad
        
        # Penalizaciones por flags
        if "viento_fuerte" in flags:
            score -= 30
        
        if "riesgo_deriva" in flags:
            score -= 40  # Muy peligroso
        
        if "olas_grandes" in flags:
            score -= 25
        
        if "principiante_condiciones_moderadas" in flags:
            score -= 15
        
        if "deriva_varese" in flags:
            score -= 20
        
        # Penalización adicional por viento según experiencia
        if user.experience == "beginner" and weather.wind.speed_kmh > 15:
            score -= (weather.wind.speed_kmh - 15) * 1.5
        
        # Ajuste por offshore (siempre reduce seguridad)
        if weather.wind.relative_direction == "offshore":
            score -= 15
        
        # Clamp entre 0-100
        return max(0, min(100, int(score)))
    
    def _calculate_effort_score(
        self, 
        weather: WeatherData, 
        user: UserProfile
    ) -> int:
        """
        Calcula score de ESFUERZO (0-100, donde 100 = muy exigente)
        Basado en viento vs potencia de remada
        """
        base_effort = weather.wind.speed_kmh * 2  # Base proporcional al viento
        
        # Ajuste por potencia de remada
        power_multiplier = {
            "low": 1.5,    # Baja potencia = más esfuerzo
            "medium": 1.0,
            "high": 0.7    # Alta potencia = menos esfuerzo
        }
        effort = base_effort * power_multiplier.get(user.paddle_power, 1.0)
        
        # Offshore requiere más esfuerzo (difícil volver)
        if weather.wind.relative_direction == "offshore":
            effort *= 1.3
        
        # Olas aumentan esfuerzo
        effort += weather.waves.height_m * 15
        
        # Clamp entre 0-100
        return max(0, min(100, int(effort)))
    
    def _calculate_enjoyment_score(
        self, 
        weather: WeatherData, 
        user: UserProfile,
        seguridad: int
    ) -> int:
        """
        Calcula score de DISFRUTE (0-100, donde 100 = muy disfrutable)
        ⚠️ CRÍTICO: Basado en objetivo de sesión, NO inverso de riesgo
        """
        goal = user.session_goal
        wind_speed = weather.wind.speed_kmh
        wave_height = weather.waves.height_m
        
        # Si seguridad es muy baja, disfrute también baja (no importa objetivo)
        if seguridad < 30:
            return max(0, seguridad - 10)
        
        # Cálculo según objetivo
        if goal == "calma":
            # Prefiere condiciones suaves
            enjoyment = 90
            enjoyment -= wind_speed * 2  # Menos viento = mejor
            enjoyment -= wave_height * 20  # Menos olas = mejor
            
        elif goal == "entrenamiento":
            # Prefiere condiciones moderadas  que desafíen sin abrumar
            if 15 < wind_speed < 25 and wave_height < 1.5:
                enjoyment = 85  # Condiciones ideales para entrenar
            elif wind_speed < 10:
                enjoyment = 40  # Demasiado tranquilo para entrenar
            else:
                enjoyment = 50  # Demasiado exigente
                
        elif goal == "desafio":
            # Avanzados disfrutan condiciones exig entes (pero seguras)
            if user.experience == "advanced" and seguridad >= 50:
                # Más viento y olas = más diversión
                enjoyment = 50 + (wind_speed * 1.5) + (wave_height * 15)
            else:
                # No avanzado o inseguro
                enjoyment = 30
        else:
            enjoyment = 50  # Fallback
        
        # Ajuste por experiencia
        if user.experience == "beginner" and wind_speed > 20:
            enjoyment *= 0.7  # Principiantes no disfrutan viento fuerte
        
        # Clamp entre 0-100
        return max(0, min(100, int(enjoyment)))
    
    def _categorize_score(self, score: int) -> str:
        """
        Convierte score numérico a categoría
        """
        if score >= 70:
            return "alto"
        elif score >= 40:
            return "medio"
        else:
            return "bajo"
    
    def _calculate_confidence(
        self, 
        weather: WeatherData
    ) -> Tuple[str, ConfidenceFactors]:
        """
        Calcula confianza del modelo de forma FORMAL
        No es metadata, es parte del resultado
        """
        score = 100.0
        
        # Factor 1: Completitud de datos
        completeness = 1.0
        if weather.wind.speed_kmh == 0:
            completeness -= 0.5
        if weather.waves.height_m == 0:
            completeness -= 0.3
        
        # Factor 2: Frescura de datos
        try:
            data_time = datetime.fromisoformat(weather.timestamp.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            age_hours = (now - data_time).total_seconds() / 3600
            
            if age_hours > 3:
                freshness = max(0, 1.0 - (age_hours - 3) / 10)
            else:
                freshness = 1.0
        except:
            freshness = 0.5  # Si no podemos parsear, confianza media
        
        # Factor 3: Volatilidad (placeholder - requeriría historial)
        volatility = 0.0  # Por ahora asumimos baja volatilidad
        
        # Calcular score de confianza
        score = (completeness + freshness) / 2 * 100
        
        # Categorizar
        if score > 70:
            confidence_level = "alta"
        elif score > 40:
            confidence_level = "media"
        else:
            confidence_level = "baja"
        
        factors = ConfidenceFactors(
            data_completeness=completeness,
            data_freshness=freshness,
            volatility=volatility
        )
        
        return confidence_level, factors
