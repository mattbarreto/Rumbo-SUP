import google.generativeai as genai
from typing import Optional
import os
from app.models.schemas import UserProfile, WeatherData, EngineResult

class PedagogyService:
    """
    Servicio pedagógico usando Gemini (Layer B)
    Refactorizado para 'Human Perception Coach' (Sensei 2.0)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
            self.model = genai.GenerativeModel(model_name)
        else:
            self.model = None
    
    async def generate_explanation(
        self,
        user: UserProfile,
        weather: WeatherData,
        result: EngineResult
    ) -> str:
        """
        Genera explicación pedagógica centrada en percepción y agencia
        """
        if not self.model:
            return self._fallback_explanation(weather, result)
        
        prompt = self._build_prompt(user, weather, result)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.5, # Bajamos temperatura para más coherencia
                    "top_p": 0.9,
                    "max_output_tokens": 800,
                }
            )
            
            explanation = response.text
            
            # Simple validation to ensure it's not empty or totally broken
            if len(explanation) < 50:
                 return self._fallback_explanation(weather, result)

            return explanation
            
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return self._fallback_explanation(weather, result)
    
    def _build_prompt(
        self,
        user: UserProfile,
        weather: WeatherData,
        result: EngineResult
    ) -> str:
        """Prompt HAX v6: Escenarios + personalización + cierre pedagógico"""
        s = result.semantics
        
        # Visual cues ya son frases humanas
        visuals_text = "\n".join([f"  - {v}" for v in s.visual_cues])
        
        # Seleccionar tip según nivel del usuario
        level_tip = s.beginner_tip if user.experience == "beginner" else s.advanced_tip
        
        prompt = f"""
Sos un instructor de SUP parado en la playa con tu alumno, mirando el mar juntos antes de entrar.

## ESCENARIO DE HOY (Usá esta información, NO la reformules, integrala naturalmente):

**Qué está moviendo el agua:**
{s.driver_desc}

**Cómo se ve la superficie:**
{s.behavior_desc}

**Qué va a sentir en el cuerpo:**
{s.body_desc}

**El riesgo de hoy:**
{s.risk_desc}

**Qué NO hacer hoy:**
{s.avoid_desc}

**Señales visuales:**
{visuals_text}

**El plan para hoy:**
{s.strategy_desc}

**Consejo para este nivel:**
{level_tip}

**Cierre pedagógico:**
{s.learning_focus}

---

## TU TAREA:

NO traduzcas ni reformules. INTEGRÁ la información en una conversación natural, como si hablaras con tu alumno en la playa.

## ESTRUCTURA:

## 🌊 Cómo está el mar hoy
[El escenario físico en 1-2 oraciones evocadoras]

## 🏄 Qué vas a sentir
[Las sensaciones físicas: pies, brazos, equilibrio]

## ⚠️ El riesgo y qué evitar
[Por qué aparece el riesgo + qué NO hacer]

## 👀 Qué buscar con los ojos
[Las señales visuales que confirman el escenario]

## 💡 Tu plan de hoy
[La estrategia concreta + el consejo para este nivel]

## 🎯 Qué estás practicando
[El cierre pedagógico - qué aprendés si sale bien]

---
Máximo 350 palabras. Español rioplatense. Tono cercano de mentor.
"""
        return prompt
    
    def _validate_structure(self, text: str) -> bool:
        """Valida que el LLM respetó la estructura - flexible matching"""
        required = [
            "mar hoy",        # "Cómo está el mar hoy"
            "sentir",         # "Qué vas a sentir"
            "riesgo",         # "El riesgo"
            "ojos",           # "Qué buscar con los ojos"
            "plan",           # "Tu plan de hoy"
            "practicando"     # "Qué estás practicando"
        ]
        text_lower = text.lower()
        return all(req in text_lower for req in required)
    
    def _fallback_explanation(self, weather: WeatherData, result: EngineResult) -> str:
        """Fallback HAX v6: Usa escenarios del motor con todos los campos"""
        s = result.semantics
        visuals = "\n".join([f"- {v}" for v in s.visual_cues[:3]])
        
        return f"""## 🌊 Cómo está el mar hoy
{s.driver_desc}

{s.behavior_desc}

## 🏄 Qué vas a sentir
{s.body_desc}

## ⚠️ El riesgo y qué evitar
{s.risk_desc}

**Qué NO hacer:** {s.avoid_desc}

## 👀 Qué buscar con los ojos
{visuals}

## 💡 Tu plan de hoy
{s.strategy_desc}

## 🎯 Qué estás practicando
{s.learning_focus}
"""
