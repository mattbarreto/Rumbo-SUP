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
        
        # Safe defaults for None values (API failures)
        wind_speed = weather.wind.speed_kmh if weather.wind.speed_kmh is not None else 0.0
        wind_deg = weather.wind.direction_deg if weather.wind.direction_deg is not None else 0
        wave_height = weather.waves.height_m if weather.waves.height_m is not None else 0.0
        
        # Calcular dirección relativa del viento
        wind_relative = self._calculate_wind_relative_direction(
            wind_deg,
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
        
        # Use safe defaults for None values (API failures)
        wind_speed = weather.wind.speed_kmh if weather.wind.speed_kmh is not None else 0.0
        wave_height = weather.waves.height_m if weather.waves.height_m is not None else 0.0

        # 1. Clasificar las condiciones en UN escenario coherente
        # Use safe defaults already calculated at start of analyze()
        scenario_id = classify_scenario(
            wind_speed=wind_speed,  # safe default from analyze()
            wind_rel=weather.wind.relative_direction or "none",
            wave_height=wave_height,  # safe default from analyze()
            tide_state=weather.tide.state,
            flags=flags
        )
        
        # 2. Obtener el paquete completo de micro-narrativas
        scenario = get_scenario(scenario_id)
        
        # 3. Inyección Dinámica de Consejos (UV, Lluvia)
        strategy_addite = ""
        risk_addite = ""
        
        if "uv_alto" in flags:
            uv_val = weather.atmosphere.uv_index
            strategy_addite += f" ☀️ El sol está muy fuerte (UV {uv_val:.1f}). Usá lycra, gorro y mucho protector solar."
            
        if "lluvia" in flags:
            driver = "lluvia" if "lluvia" in flags else "" # Placeholder
            risk_addite += " 🌧️ La lluvia reduce la visibilidad y enfría el cuerpo rápido. "
            
        if "mar_picado" in flags:
            risk_addite += " 🌊 El mar está picado (periodo corto), te va a costar más mantener el equilibrio."

        # 4. Retornar semántica enriquecida
        return SemanticAnalysis(
            scenario_id=scenario.id,
            driver_desc=scenario.driver_desc,
            behavior_desc=scenario.behavior_desc,
            body_desc=scenario.body_desc,
            risk_desc=scenario.risk_desc + risk_addite,
            avoid_desc=scenario.avoid_desc,
            visual_cues=scenario.visual_cues,
            strategy_desc=scenario.strategy_desc + strategy_addite,
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
        
        IMPORTANTE: Usamos rangos de grados específicos para Mar del Plata (Varese).
        Esta lógica debe coincidir EXACTAMENTE con windUtils.calculateMarDelPlataOffshore()
        en el frontend para evitar inconsistencias.
        
        Rangos para costa orientada al Este (Varese):
        - Onshore (desde el mar): 22.5° - 157.5° (NNE a SSE)
        - Cross (paralelo): 157.5° - 202.5° (S) y 337.5° - 22.5° (N)
        - Offshore (desde tierra): 202.5° - 337.5° (SSO a NNO)
        
        Returns:
            "onshore" (hacia playa), "offshore" (hacia mar), "cross" (paralelo)
        """
        # Normalizar a 0-360
        deg = wind_deg % 360
        if deg < 0:
            deg += 360
        
        # Rangos específicos para Mar del Plata / Varese
        # Estos rangos reflejan la geografía real de la playa
        if deg >= 22.5 and deg <= 157.5:
            return "onshore"   # Viento del mar hacia la playa (NNE a SSE)
        elif deg > 157.5 and deg < 202.5:
            return "cross"     # Viento paralelo (Sur)
        elif deg >= 202.5 and deg <= 337.5:
            return "offshore"  # Viento de tierra hacia el mar (SSO a NNO)
        else:
            return "cross"     # Sector Norte (337.5 - 360 - 22.5)
            
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
        
        # Safe defaults for None
        wind_speed = weather.wind.speed_kmh if weather.wind.speed_kmh is not None else 0.0
        wave_height = weather.waves.height_m if weather.waves.height_m is not None else 0.0
        wave_period = weather.waves.period_s if weather.waves.period_s is not None else 0.0
        
        # --- Flags Críticos de Seguridad ---
        
        # Tormenta Eléctrica (Códigos WMO 95, 96, 99)
        wcode = weather.atmosphere.weather_code
        if wcode in [95, 96, 99]:
            flags.append("tormenta_electrica")
            
        # Visibilidad Nula (< 1km)
        vis = weather.atmosphere.visibility_km
        if vis is not None and vis < 1.0:
            flags.append("visibilidad_nula")
        
        # --- Flags de Condiciones ---
        
        # Viento fuerte
        if wind_speed > 30:
            flags.append("viento_fuerte")
        
        # Riesgo de deriva (offshore + inflable)
        if (weather.wind.relative_direction == "offshore" and 
            user.board_type == "inflable"):
            flags.append("riesgo_deriva")
        
        # Olas grandes
        if wave_height > 1.5:
            flags.append("olas_grandes")
            
        # Mar Picado (Choppy): Periodo corto con cierta altura
        if wave_period > 0 and wave_period < 5.0 and wave_height > 0.5:
            flags.append("mar_picado")
        
        # Lluvia
        precip = weather.atmosphere.precipitation_mm
        if precip is not None and precip > 0.5:
            flags.append("lluvia")
            
        # UV Alto
        uv = weather.atmosphere.uv_index
        if uv is not None and uv >= 6.0:
            flags.append("uv_alto")
        
        # Principiante en condiciones moderadas
        if (user.experience == "beginner" and 
            (wind_speed > 20 or wave_height > 1.0)):
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
        wind_speed = weather.wind.speed_kmh if weather.wind.speed_kmh is not None else 0.0
        if user.experience == "beginner" and wind_speed > 15:
            score -= (wind_speed - 15) * 1.5
        
        # Ajuste por offshore (siempre reduce seguridad)
        if weather.wind.relative_direction == "offshore":
            score -= 15
            
        # Penalización por Mar Picado (inestabilidad)
        if "mar_picado" in flags:
            score -= 10
            
        # Penalización por Visibilidad/Lluvia
        if "visibilidad_nula" in flags or "tormenta_electrica" in flags:
            score = 0  # CRÍTICO: Anular seguridad
        elif "lluvia" in flags:
            score -= 10
        
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
        wind_speed = weather.wind.speed_kmh if weather.wind.speed_kmh is not None else 0.0
        wave_height = weather.waves.height_m if weather.waves.height_m is not None else 0.0
        base_effort = wind_speed * 2  # Base proporcional al viento
        
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
        effort += wave_height * 15
        
        # Mar Picado aumenta esfuerzo significativamente (constante corrección)
        if weather.waves.period_s and weather.waves.period_s < 5.0 and wave_height > 0.5:
            effort += 20
        
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
        wind_speed = weather.wind.speed_kmh if weather.wind.speed_kmh is not None else 0.0
        wave_height = weather.waves.height_m if weather.waves.height_m is not None else 0.0
        
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
