# 🤖 Instrucciones Críticas para Agente de Codificación

## Propósito de este Documento

Este documento contiene **restricciones arquitectónicas y principios de diseño inmutables** que CUALQUIER agente de codificación que implemente Rumbo SUP **DEBE respetar**.

Estas reglas existen para evitar que el agente:
- Simplifique indebidamente la lógica
- Colapse la separación Layer A / Layer B
- Mezcle explicación con decisión
- Cree un "semáforo GO/NO-GO" genérico

> [!CAUTION]
> **Si un agente viola estas reglas, el sistema perderá su propósito educativo y de seguridad.**

---

## 🚨 Reglas Inmutables (NUNCA Violar)

### Regla 1: Layer A y Layer B Nunca Se Mezclan

#### Layer A (Motor Determinístico)
- **Responsabilidad**: Calcular scores de seguridad, esfuerzo y disfrute
- **Método**: Algoritmos determinísticos, umbrales definidos, reglas formales
- **Salida**: Números y categorías (sin explicación en lenguaje natural)
- **NO puede**: Usar IA, tomar decisiones subjetivas, cambiar basado en feedback

#### Layer B (Sistema Pedagógico)
- **Responsabilidad**: Explicar los resultados del Layer A en lenguaje educativo
- **Método**: LLM (Gemini/GPT) con prompts estructurados
- **Salida**: Texto educativo, glosario, checklists visuales
- **NO puede**: Calcular scores, decidir si es seguro, contradecir Layer A

#### ⚠️ Implementación

```python
# ❌ MAL - Layer B influye en decisión
def analyze_conditions(weather, user):
    # Pregunta a LLM si es seguro
    ai_result = gemini.ask("¿Es seguro remar con viento de 25 km/h?")
    return parse_ai_decision(ai_result)

# ✅ BIEN - Layer A decide, Layer B explica
def analyze_conditions(weather, user):
    # Layer A: Cálculo determinístico
    engine = SenseiEngine()
    result = engine.analyze(weather, spot, user)  # Pure logic
    
    # Layer B: Explicación (separada, nunca influye en result)
    explanation = pedagogy_service.explain(result, weather, user)
    
    return result, explanation
```

**Test de violación**: Si borras el LLM, ¿el sistema sigue decidiendo correctamente? → Debe ser SÍ.

---

### Regla 2: Semáforo = SOLO Seguridad (Nunca GO/NO-GO)

#### Prohibido
- Texto "GO" o "NO-GO" en el indicador circular
- Colapsar riesgo + esfuerzo + disfrute en un solo score
- Dar una "recomendación final"

#### Obligatorio
- Indicador circular muestra **solo seguridad**
- Textos permitidos:
  - Verde: "Condiciones seguras"
  - Amarillo: "Con precaución"
  - Rojo: "No recomendado"
- Cards separadas para esfuerzo y disfrute

#### Razonamiento
Alguien puede querer:
- Entrenar fuerte (alto esfuerzo) en condiciones seguras ✅
- Relajarse (bajo esfuerzo) en condiciones seguras ✅

NO puede querer:
- Alto riesgo aunque disfrute sea alto ❌

Por eso: **Seguridad es no-negociable, esfuerzo/disfrute son preferencias.**

#### ⚠️ Implementación

```jsx
// ❌ MAL - GO/NO-GO colapsa todo
<SecurityIndicator>
  {overallScore > 70 ? "GO" : "NO-GO"}
</SecurityIndicator>

// ✅ BIEN - Solo seguridad + cards separadas
<SecurityIndicator security={result.scores.seguridad}>
  {security > 70 ? "Condiciones seguras" : "..."}
</SecurityIndicator>

<MetricCard label="Esfuerzo" value={result.scores.esfuerzo} />
<MetricCard label="Disfrute" value={result.scores.disfrute} />
```

---

### Regla 3: Disfrute NO es Inverso de Riesgo

#### Prohibido
```python
# ❌ Simplificación incorrecta
disfrute = 100 - riesgo - esfuerzo
```

#### Obligatorio
Disfrute se calcula según **adecuación a objetivo de sesión**:

```python
def calculate_enjoyment(weather, session_goal, experience):
    """
    session_goal: 'calma' | 'entrenamiento' | 'desafío'
    """
    if session_goal == 'calma':
        # Prefiere condiciones suaves
        if weather.wind < 15 and weather.waves < 1.0:
            return 80  # Alto disfrute
        else:
            return 30  # Bajo disfrute
    
    elif session_goal == 'entrenamiento':
        # Prefiere condiciones moderadas que desafíen sin abrumar
        if moderate_conditions_for_skill_level(weather, experience):
            return 85
        else:
            return 50
    
    elif session_goal == 'desafío':
        # Avanzados disfrutan condiciones exigentes (pero seguras)
        if challenging_but_safe(weather, experience):
            return 90
        else:
            return 40
```

**Mismo mar, 3 objetivos diferentes, 3 scores de disfrute diferentes.**

---

### Regla 4: LLM Output Debe Tener Estructura Forzada

#### Prohibido
- Prompts abiertos tipo "Explica las condiciones"
- Permitir que el LLM genere formato libre
- Salidas sin restricción de longitud

#### Obligatorio
```python
EXPLANATION_TEMPLATE = """
Genera una explicación educativa siguiendo EXACTAMENTE esta estructura:

## ¿Qué está pasando?
[Descripción objetiva de las condiciones actuales en 2-3 oraciones]

## Cómo se siente esto
[Explicación sensorial de la experiencia esperada: viento en la cara, estabilidad de la tabla, etc.]

## Consejos de seguridad
[3 tips específicos y accionables]

## Checklist visual
1. [Cosa concreta para observar antes de entrar]
2. [Cosa concreta para observar antes de entrar]
3. [Cosa concreta para observar antes de entrar]

Restricciones:
- Longitud máxima: 300 palabras
- Tono: Amigable, educativo
- Nivel: {user_experience}
- NUNCA uses palabras "entra", "no entres", "ve", "quédate" - solo educa
"""
```

#### Validación Post-Generación
```python
def validate_explanation(text):
    required_sections = [
        "## ¿Qué está pasando?",
        "## Cómo se siente esto",
        "## Consejos de seguridad",
        "## Checklist visual"
    ]
    
    for section in required_sections:
        if section not in text:
            raise ValueError(f"Missing section: {section}")
    
    if len(text.split()) > 350:
        raise ValueError("Explanation too long")
    
    forbidden_words = ["entra", "no entres", "ve al agua", "quédate"]
    if any(word in text.lower() for word in forbidden_words):
        raise ValueError("Explanation contains decision language")
```

---

### Regla 5: Confianza es Output Formal, No Metadata

#### Prohibido
```python
# ❌ Confianza como metadata técnica
def analyze():
    result = calculate_scores()
    result.metadata = {"confidence": "high" if all_data_present else "low"}
```

#### Obligatorio
```python
# ✅ Confianza como output formal del motor
def analyze(weather, spot, user):
    scores = calculate_scores(weather, user)
    
    # Cálculo formal de confianza
    confidence_score = 100
    
    # Completitud de datos
    if weather.missing_variables:
        confidence_score -= 30
    
    # Cercanía temporal
    data_age_hours = (now - weather.timestamp).hours
    if data_age_hours > 3:
        confidence_score -= 20
    
    # Volatilidad detectada
    if detect_rapid_wind_change(weather.history):
        confidence_score -= 25
    
    confidence_level = (
        "alta" if confidence_score > 70 
        else "media" if confidence_score > 40 
        else "baja"
    )
    
    return EngineResult(
        scores=scores,
        confidence=confidence_level,  # Parte del resultado principal
        confidence_factors={  # Detalles para UX
            "data_completeness": ...,
            "data_freshness": ...,
            "volatility": ...
        }
    )
```

**UX debe mostrar confianza baja explícitamente** (badge o alert).

---

### Regla 6: Modelo de Seguridad es Inmutable

#### Prohibido
Cualquier ajuste del modelo de seguridad basado en:
- Feedback del usuario
- Preferencias personales
- Historial de sesiones

#### Permitido
Ajustar basado en feedback:
- **Esfuerzo**: Si usuario reporta esfuerzo menor al predicho → incrementar "potencia de remada" en perfil
- **Disfrute**: Si usuario reporta bajo disfrute → ajustar preferencia de objetivo

```python
def process_post_session_feedback(predicted, actual, user_profile):
    # ✅ BIEN - Ajustar modelado de esfuerzo
    if actual.effort < predicted.effort - 20:
        user_profile.paddle_power = increase_one_level(user_profile.paddle_power)
    
    # ✅ BIEN - Ajustar preferencias de disfrute
    if actual.enjoyment < predicted.enjoyment - 20:
        user_profile.preferred_session_goal = adjust_preference()
    
    # ❌ PROHIBIDO - Ajustar modelo de seguridad
    # if actual.felt_safe and predicted.security == "bajo":
    #     adjust_safety_thresholds()  # NUNCA
```

**Razonamiento**: La seguridad es objetiva. El esfuerzo y disfrute son subjetivos.

---

### Regla 7: Proveedor de Datos Meteorológicos Debe Estar Abstraído

#### Prohibido
```python
# ❌ Acoplamiento directo a OpenMeteo
def get_weather(lat, lon):
    url = "https://marine-api.open-meteo.com/v1/marine"
    response = requests.get(url, params=...)
    return parse_openmeteo_response(response)

def analyze(lat, lon, user):
    weather = get_weather(lat, lon)  # Directamente acoplado
    return engine.analyze(weather, user)
```

#### Obligatorio
```python
# ✅ Adapter pattern
from abc import ABC, abstractmethod

class WeatherProvider(ABC):
    @abstractmethod
    def get_conditions(self, lat: float, lon: float) -> WeatherData:
        pass

class OpenMeteoProvider(WeatherProvider):
    def get_conditions(self, lat, lon):
        # Implementación específica OpenMeteo
        pass

class StormglassProvider(WeatherProvider):
    def get_conditions(self, lat, lon):
        # Implementación futura
        pass

# Inyección de dependencia
class WeatherService:
    def __init__(self, provider: WeatherProvider):
        self.provider = provider
    
    def get_current_conditions(self, lat, lon):
        return self.provider.get_conditions(lat, lon)

# Uso
weather_service = WeatherService(OpenMeteoProvider())
```

**Beneficio**: Facilita swap de proveedores, agregar múltiples fuentes, testing.

---

## 🎓 Principios HAX (Human-AI Experience)

### Entrenamiento Perceptivo

El sistema debe **reducir dependencia del usuario con el tiempo**, no incrementarla.

#### ¿Cómo?
- **Checklists visuales**: "Mirá si las olas rompen de forma consistente"
- **Explicaciones corporales**: "Sentirás el viento empujándote hacia..."
- **Glosario activo**: Cada término técnico debe tener tooltip

#### Implementación
```python
# En configuración de spot
SPOTS = {
    "varese": {
        ...,
        "visual_checklist": [
            "Mirá las olas cerca de la costa: ¿rompen de forma consistente?",
            "Observá la espuma: ¿se desplaza rápido hacia el mar?",
            "Revisá las banderas: ¿están estiradas por el viento?"
        ]
    }
}

# En prompt de LLM
context += f"""
Incluye en la sección "Checklist visual" referencias a:
{spot.visual_checklist}
"""
```

### Feedback Loop Adaptativo

Post-sesión, el sistema debe preguntar:
- "¿Cómo estuvo el esfuerzo?" (slider 1-10)
- "¿Disfrutaste?" (slider 1-10)
- "Notas adicionales" (texto libre)

Y ajustar perfil (NO modelo de seguridad).

---

## 🧪 Tests de Validación Arquitectónica

### Test 1: Independencia del LLM
```bash
# Deshabilitar LLM
export GEMINI_API_KEY=""

# El sistema debe seguir funcionando
curl POST /api/analyze
# ✅ Debe retornar scores correctos
# ❌ Si falla, Layer A depende de Layer B (violación)
```

### Test 2: Consistencia de Seguridad
```python
# Mismo input, mismo output (determinismo)
result1 = engine.analyze(weather, spot, user)
result2 = engine.analyze(weather, spot, user)

assert result1.scores.seguridad == result2.scores.seguridad
# ✅ Debe pasar
# ❌ Si falla, motor es no-determinístico (violación)
```

### Test 3: Variabilidad de Disfrute
```python
# Mismo weather, diferentes objetivos, diferentes scores
result_calma = engine.analyze(weather, spot, user_calma)
result_desafio = engine.analyze(weather, spot, user_desafio)

assert result_calma.scores.disfrute != result_desafio.scores.disfrute
# ✅ Debe pasar (modelado sofisticado)
# ❌ Si no varía, disfrute es simplificado incorrectamente
```

### Test 4: Estructura de Explicación
```python
explanation = pedagogy.explain(result, weather, user)

required_sections = ["## ¿Qué está pasando?", "## Cómo se siente esto", ...]
for section in required_sections:
    assert section in explanation
# ✅ Debe pasar
# ❌ Si falla, LLM no está forzado a estructura
```

### Test 5: Inmutabilidad de Seguridad
```python
# Feedback no debe cambiar modelo de seguridad
original_safety = engine.analyze(weather, spot, user).scores.seguridad

process_feedback(session_id, {"felt_safe": True})

new_safety = engine.analyze(weather, spot, user).scores.seguridad

assert original_safety == new_safety
# ✅ Debe pasar
# ❌ Si cambia, seguridad es mutable (violación crítica)
```

---

## 📋 Checklist para Agente Durante Implementación

Antes de considerar una feature "completa", verificar:

### Motor (Layer A)
- [ ] `seguridad` (no `riesgo`) está invertido correctamente
- [ ] `disfrute` usa objetivo de sesión, no solo inverso de riesgo/esfuerzo
- [ ] `confianza` se calcula formalmente (completitud, temporal, volatilidad)
- [ ] Todas las reglas son determinísticas (no usan LLM)
- [ ] Proveedor meteorológico está abstraído (adapter pattern)

### Pedagogía (Layer B)
- [ ] Prompt fuerza estructura (4 secciones obligatorias)
- [ ] Longitud máxima enforced (300 palabras)
- [ ] Validación post-generación rechaza "entra"/"no entres"
- [ ] Checklist visual incluida en output
- [ ] Glosario de términos está disponible

### Frontend
- [ ] Indicador circular dice "Condiciones seguras" (no "GO")
- [ ] Seguridad, esfuerzo, disfrute están en cards SEPARADAS
- [ ] Selector de objetivo de sesión presente (calma/entrenamiento/desafío)
- [ ] Confianza baja se muestra visualmente (badge/alert)
- [ ] Página PostSession implementada (feedback loop)
- [ ] Botón "Salir del agua" presente en Landing

### Integración
- [ ] Test de independencia LLM pasa
- [ ] Test de determinismo pasa
- [ ] Test de variabilidad de disfrute pasa
- [ ] Test de estructura de explicación pasa
- [ ] Test de inmutabilidad de seguridad pasa

---

## 🚫 Anti-Patterns Comunes de Agentes

### 1. Simplificación Prematura
```python
# ❌ Agente puede intentar
disfrute = 100 - riesgo  # "Más simple"

# ✅ Debe implementar lógica completa
disfrute = calculate_enjoyment_based_on_session_goal(...)
```

### 2. Colapso de Capas
```python
# ❌ Agente puede mezclar
def analyze_and_explain(weather):
    # LLM genera scores Y explicación
    return gemini.ask("Analiza y explica estos datos...")

# ✅ Separación estricta
def analyze(weather):
    return engine.calculate(weather)  # Layer A

def explain(result):
    return pedagogy.generate(result)  # Layer B
```

### 3. "Smart Defaults" que Violan Principios
```python
# ❌ Agente puede proponer
# "Por defecto, mostrar GO/NO-GO es más simple"

# ✅ Debe respetar
# Semáforo = solo seguridad, siempre
```

### 4. Omitir Validaciones
```python
# ❌ Agente puede omitir por velocidad
explanation = llm.generate(prompt)
return explanation  # Sin validar

# ✅ Debe validar siempre
explanation = llm.generate(prompt)
validate_structure(explanation)  # Forzar
return explanation
```

---

## 💬 Comunicación con Usuario Durante Implementación

Si el agente descubre ambigüedad o conflicto, debe preguntar al usuario:

**Buena pregunta**:
> "La regla de viento offshore para tabla inflable actualmente suma +50 a riesgo. ¿Es conservador suficiente o debería ser +70?"

**Mala pregunta**:
> "¿Quieres que simplifique el modelo de disfrute? Podría ser inverso de riesgo."

**Respuesta correcta**: "No, el modelo de disfrute debe ser basado en objetivos de sesión (ver specs)."

---

## 📚 Referencias

- `abstraction.md`: Análisis del proyecto original
- `project_prompt.md`: Especificaciones completas
- `implementation_plan.md`: Fases y componentes

---

**Último recordatorio para el agente**:

> Si alguna vez tienes dudas sobre si estás violando una regla, pregunta al usuario. Pero si la regla está explícita aquí, **no hay negociación**: debe cumplirse.
