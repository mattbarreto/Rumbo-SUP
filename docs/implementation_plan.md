# Plan de Implementación: Rumbo SUP - Mobile PWA

## Objetivo

Recrear Rumbo SUP como una **Progressive Web App (PWA) móvil-first** más ágil y fácil de iterar que la versión React Native actual. La aplicación debe funcionar exclusivamente en dispositivos móviles con GPS, enfocada en Mar del Plata (especialmente Varese), con arquitectura escalable para futuro SaaS multi-ciudad.

> [!IMPORTANT]
> **Principios de Diseño Críticos**
> - **Semáforo = Solo seguridad** (nunca GO/NO-GO genérico)
> - **Layer A y Layer B nunca se mezclan** (decisión vs explicación)
> - **Disfrute = Adecuación a objetivo de sesión** (no solo inverso de riesgo)
> - **Sistema adaptativo** (aprende del feedback post-sesión)
> - **Entrena percepción** (reduce dependencia con el tiempo)

---

## Contexto

### Proyecto Actual
- **Stack**: React Native (Expo) + FastAPI
- **Estado**: Frontend con errores de bundling, backend funcional
- **Problemas**: Complejo de deployar, difícil de testear iterativamente

### Propuesta Nueva
- **Stack**: Vite + React + FastAPI (o serverless)
- **Ventajas**: 
  - Deploy inmediato sin App Store
  - Testing directo en browser móvil
  - Desarrollo más ágil
  - PWA instalable

---

## Propuestas de Cambio

### Arquitectura General

```
┌─────────────────────────────────────┐
│   Mobile Browser                    │
│   ┌─────────────────────────────┐   │
│   │  PWA Frontend               │   │
│   │  - Vite + React             │   │
│   │  - Geolocation API          │   │
│   │  - Service Workers          │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
                  ↓ HTTPS
┌─────────────────────────────────────┐
│   Backend API                       │
│   ┌─────────────────────────────┐   │
│   │  FastAPI (Python)           │   │
│   │  - Layer A: Motor Engine    │   │
│   │  - Layer B: Gemini Client   │   │
│   │  - OpenMeteo Integration    │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│   External APIs                     │
│   - OpenMeteo Marine API            │
│   - Google Gemini API               │
└─────────────────────────────────────┘
```

---

## Cambios Propuestos por Componente

### Frontend

#### [NEW] [index.html](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/index.html)

HTML base con:
- Meta tags PWA
- Viewport para móvil
- Links a manifest y service worker
- Detección de dispositivo móvil

#### [NEW] [manifest.json](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/manifest.json)

Configuración PWA:
- Nombre: "Rumbo SUP"
- Íconos en múltiples tamaños
- Display: standalone
- Theme color: ocean blue
- Orientación: portrait

#### [NEW] [src/main.jsx](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/src/main.jsx)

Entry point de React:
- Inicialización de app
- Router setup
- Registro de Service Worker

#### [NEW] [src/App.jsx](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/src/App.jsx)

Componente principal:
- React Router configuración
- Layout con navegación
- Rutas: /, /onboarding, /sensei, /profile

#### [NEW] [src/pages/Landing.jsx](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/src/pages/Landing.jsx)

Pantalla principal:
- Detección de geolocalización
- **Selector de objetivo de sesión** (calma/entrenamiento/desafío) - afecta score de disfrute
- Llamada a `/api/analyze` con objetivo incluido
- **Indicador circular de SEGURIDAD** (no "GO/NO-GO"):
  - Verde: "Condiciones seguras"
  - Amarillo: "Con precaución"
  - Rojo: "No recomendado"
- **Cards separadas** para:
  - Seguridad (repetición del semáforo con número)
  - Esfuerzo
  - Disfrute (contextualizado al objetivo elegido)
- Flags de alerta
- Indicador de confianza (si baja, badge visible)
- Botón "¿Por qué?" → Sensei
- **NUEVO: Botón "Salir del agua"** → Post-Session Feedback

#### [NEW] [src/pages/Onboarding.jsx](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/src/pages/Onboarding.jsx)

Flujo de onboarding:
- Bienvenida
- Solicitud de permisos de ubicación
- Formulario de perfil:
  - Tipo de tabla (rígida/inflable)
  - Nivel de experiencia (principiante/intermedio/avanzado)
  - Potencia de remada (baja/media/alta)
  - **NUEVO: Objetivo de sesión por defecto** (calma/entrenamiento/desafío)
- Guardado en LocalStorage

#### [NEW] [src/pages/Sensei.jsx](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/src/pages/Sensei.jsx)

Pantalla de explicaciones:
- Recibe engine result de Landing
- Llamada a `/api/pedagogy/explain`
- Renderiza markdown con explicación IA (estructura forzada)
- **Secciones esperadas**:
  - "¿Qué está pasando?"
  - "Cómo se siente esto"
  - "Consejos de seguridad"
  - **"Checklist visual"** (entrenamiento perceptivo)
- Glosario expandible
- Enfatizar que Sensei NUNCA dice "entra" o "no entres"

#### [NEW] [src/pages/Profile.jsx](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/src/pages/Profile.jsx)

Configuración de usuario:
- Editar perfil
- Ver/editar datos guardados
- Link a "Acerca de"

#### [NEW] [src/components/SecurityIndicator.jsx](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/src/components/SecurityIndicator.jsx)

**Renombrado** de RiskIndicator → SecurityIndicator

Componente visual del indicador:
- Círculo SVG animado
- Color según seguridad (verde/amarillo/rojo)
- Texto:
  - Verde: "Condiciones seguras"
  - Amarillo: "Con precaución"
  - Rojo: "No recomendado"
- **Nunca** "GO" / "NO-GO" (eso es decisión del usuario)

#### [NEW] [src/components/MetricCard.jsx](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/src/components/MetricCard.jsx)

Card para métricas:
- Score numérico
- Categoría (bajo/medio/alto)
- Icono contextual

#### [NEW] [src/hooks/useLocation.js](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/src/hooks/useLocation.js)

Hook para geolocalización:
- Request de permisos
- Obtención de coordenadas
- Error handling

#### [NEW] [src/pages/PostSession.jsx](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/src/pages/PostSession.jsx)

**Feedback post-sesión** (loop adaptativo):
- Pregunta: "¿Cómo estuvo la sesión?"
- Sliders:
  - "Esfuerzo real" (1-10)
  - "Disfrute real" (1-10)
- Campo de texto: "Notas adicionales" (opcional)
- Botón "Guardar feedback"
- **Lógica**:
  - Si esfuerzo real << esfuerzo predicho: ajustar perfil (incrementar potencia de remada)
  - Si disfrute real != disfrute predicho: ajustar preferencia de objetivo
  - **NUNCA ajustar modelo de seguridad** - ese es inmutable

#### [NEW] [src/services/api.js](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/src/services/api.js)

Cliente API:
- `analyzeConditions(spotId, userProfile, sessionGoal)`
- `explainResult(context)`
- `getNearestSpot(lat, lon)`
- `submitPostSessionFeedback(sessionId, feedback)`

#### [NEW] [src/styles/theme.css](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/src/styles/theme.css)

Design system:
- Variables CSS (colores océano, semáforo, neutrales)
- Tipografía
- Animaciones oceánicas (olas, gradientes)

#### [NEW] [src/utils/deviceDetection.js](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/src/utils/deviceDetection.js)

Detección de dispositivo:
- `isMobile()`: retorna true si es móvil/tablet
- Bloqueo para desktop

#### [NEW] [public/sw.js](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/public/sw.js)

Service Worker:
- Cache de assets estáticos
- Cache de último resultado `/api/analyze`
- Funcionalidad offline básica

#### [NEW] [package.json](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/frontend-pwa/package.json)

Dependencias:
- `vite` 
- `react`, `react-dom`
- `react-router-dom`
- `axios`
- Opcional: `framer-motion`, `react-markdown`

---

### Backend

#### [MODIFY] [backend/app/main.py](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/backend/app/main.py)

Cambios:
- Agregar CORS middleware para permitir frontend PWA
- Mantener endpoints existentes

#### [MODIFY] [backend/app/api/routes.py](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/backend/app/api/routes.py)

Cambios:
- Refactorizar endpoint `POST /api/analyze`
- Aceptar `spot_id` + `user_profile`
- Llamar a OpenMeteo con coordenadas del spot
- Retornar estructura completa (weather + engine result)

#### [NEW] [backend/app/api/spots.py](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/backend/app/api/spots.py)

Nuevo endpoint:
- `GET /api/spots/nearest?lat=X&lon=Y`
- Calcula spot más cercano a coordenadas
- Retorna ID y distancia

#### [MODIFY] [backend/app/services/weather_service.py](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/backend/app/services/weather_service.py)

Cambios:
- Implementar llamada real a OpenMeteo (ya existe estructura)
- Parsear respuesta horaria → condición actual
- Manejar errores de API

#### [NEW] [backend/app/config/spots.py](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/backend/app/config/spots.py)

Configuración de spots:
```python
SPOTS = {
    "varese": {
        "name": "Varese",
        "lat": -37.9833,
        "lon": -57.5333,
        "orientation_costa_deg": 90,
        "reglas_especificas": [...],
        "visual_checklist": [  # NUEVO: Entrenamiento perceptivo
            "Mirá las olas cerca de la costa: ¿rompen de forma consistente?",
            "Observá la espuma: ¿se desplaza rápido hacia el mar?",
            "Revisá las banderas: ¿están estiradas por el viento?"
        ]
    }
}
```

#### [MODIFY] [backend/app/engine/rules.py](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/backend/app/engine/rules.py)

Refinamientos críticos:
- Renombrar `riesgo` → `seguridad` (score invertido)
- Implementar **modelo de disfrute basado en objetivos**:
  ```python
  def calculate_enjoyment(weather, user_session_goal, experience):
      # user_session_goal: "calma" | "entrenamiento" | "desafío"
      if user_session_goal == "calma":
          return high if (low wind and low waves) else low
      elif user_session_goal == "entrenamiento":
          return high if (moderate conditions matching skill) else medium
      elif user_session_goal == "desafío":
          return high if (challenging but safe for advanced) else low
  ```
- Implementar **cálculo formal de confianza**:
  ```python
  def calculate_confidence(weather_data, timestamp):
      score = 100
      if missing_variables: score -= 30
      if data_age_hours > 3: score -= 20
      if wind_volatility_high: score -= 25
      return "alta" if score > 70 else "media" if score > 40 else "baja"
  ```
- Ajustar thresholds basados en condiciones reales de MDQ
- Reemplazar `eval()` con `asteval` (parser seguro)

#### [MODIFY] [backend/app/pedagogy/prompts.py](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/backend/app/pedagogy/prompts.py)

Refinamientos críticos:
- **Forzar estructura de salida**:
  ```python
  EXPLANATION_TEMPLATE = """
  Genera una explicación educativa siguiendo EXACTAMENTE esta estructura:
  
  ## ¿Qué está pasando?
  [Descripción objetiva de las condiciones actuales]
  
  ## Cómo se siente esto
  [Explicación sensorial/corporal de la experiencia esperada]
  
  ## Consejos de seguridad
  [Tips específicos y accionables]
  
  ## Checklist visual
  [3 cosas concretas para observar antes de entrar]
  
  Longitud máxima: 300 palabras.
  Tono: Amigable, educativo, nivel {user_experience}.
  """
  ```
- Agregar ejemplos de buenas explicaciones
- Incluir glosario en contexto
- Restricción: NUNCA debe decir "entra" o "no entres" - solo educar

#### [NEW] [backend/app/services/weather_provider.py](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/backend/app/services/weather_provider.py)

**Abstracción de proveedor meteorológico** (adapter pattern):
```python
from abc import ABC, abstractmethod

class WeatherProvider(ABC):
    @abstractmethod
    def get_conditions(self, lat: float, lon: float) -> WeatherData:
        pass

class OpenMeteoProvider(WeatherProvider):
    def get_conditions(self, lat, lon):
        # Implementación actual
        pass

class StormglassProvider(WeatherProvider):  # Futuro
    def get_conditions(self, lat, lon):
        pass
```
- Permite swap de proveedores sin tocar lógica del motor
- Facilita agregar múltiples fuentes y promediar

#### [MODIFY] [backend/app/services/weather_service.py](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/backend/app/services/weather_service.py)

Cambios:
- Usar `WeatherProvider` abstracción
- Inyectar proveedor específico (OpenMeteo para MVP)

#### [MODIFY] [backend/requirements.txt](file:///c:/Users/matia/OneDrive/Documentos/000%20-%20Desarrollos/SUP%20-%20Sensei/backend/requirements.txt)

Agregar:
```
python-multipart
fastapi-cors
asteval  # Parser seguro para reglas
```

---

## Fases de Implementación

### Fase 1: Setup & Estructura (Día 1-2)

**Frontend**
- [ ] Inicializar proyecto Vite + React
- [ ] Configurar Vite con plugin PWA
- [ ] Crear estructura de carpetas
- [ ] Implementar design system (theme.css)
- [ ] Crear componentes base (RiskIndicator, MetricCard)
- [ ] Implementar detección de dispositivo

**Backend**
- [ ] Agregar CORS middleware
- [ ] Crear `/api/spots/nearest` endpoint
- [ ] Crear archivo `config/spots.py` con Varese

**Verificación Fase 1**
- [ ] `npm run dev` levanta frontend sin errores
- [ ] Acceder desde móvil en red local (ngrok/tailscale)
- [ ] Desktop muestra mensaje "Solo móviles"
- [ ] Backend responde en `/api/health`

---

### Fase 2: Onboarding & Perfil (Día 3-4)

**Frontend**
- [ ] Página de Onboarding completa
- [ ] Hook `useLocation` funcionando
- [ ] Formulario de perfil (tabla, experiencia, potencia)
- [ ] Guardado en LocalStorage
- [ ] Página de Profile (edición)

**Backend**
- No requiere cambios

**Verificación Fase 2**
- [ ] Onboarding solicita permisos correctamente
- [ ] Datos se guardan en LocalStorage
- [ ] Perfil se puede editar y persiste

---

### Fase 3: Motor & Datos Reales (Día 5-7)

**Frontend**
- [ ] Página Landing con SecurityIndicator (no "GO/NO-GO")
- [ ] Selector de objetivo de sesión (calma/entrenamiento/desafío)
- [ ] Llamada a `/api/analyze` con perfil + objetivo
- [ ] Renderizado de indicador de SEGURIDAD separado de métricas
- [ ] Cards separadas (seguridad, esfuerzo, disfrute)
- [ ] Display de flags de alerta
- [ ] Indicador de confianza del modelo

**Backend**
- [ ] Implementar abstracción `WeatherProvider`
- [ ] Implementar `OpenMeteoProvider`
- [ ] Refinar lógica de `SenseiEngine.analyze()`:
  - [ ] Renombrar riesgo → seguridad (invertido)
  - [ ] Implementar modelo de disfrute basado en objetivos
  - [ ] Implementar cálculo formal de confianza
- [ ] Ajustar thresholds de seguridad (conservador)
- [ ] Testing con condiciones reales de MDQ

**Verificación Fase 3**
- [ ] `/api/analyze` retorna datos reales de OpenMeteo
- [ ] Motor calcula seguridad coherente (conservador)
- [ ] Disfrute varía según objetivo elegido para mismas condiciones
- [ ] Confianza baja se muestra cuando corresponde
- [ ] Frontend muestra indicador correcto con textos apropiados
- [ ] Testing en Varese con condiciones del día

---

### Fase 4: IA Pedagógica (Día 8-10)

**Frontend**
- [ ] Página Sensei con secciones estructuradas
- [ ] Botón "¿Por qué?" en Landing → navega a Sensei
- [ ] Llamada a `/api/pedagogy/explain`
- [ ] Renderizado de markdown con estructura forzada
- [ ] Display de checklist visual (entrenamiento perceptivo)
- [ ] Glosario expandible

**Backend**
- [ ] Implementar prompt estructurado en `prompts.py`:
  - [ ] Forzar secciones (Qué/Cómo se siente/Consejos/Checklist)
  - [ ] Restricción de longitud (300 palabras)
  - [ ] NUNCA permitir "entra" o "no entres"
- [ ] Agregar glosario completo
- [ ] Incluir checklist visual del spot en contexto
- [ ] Testing de calidad de explicaciones

**Verificación Fase 4**
- [ ] Explicaciones siguen estructura consistente
- [ ] Nunca dicen "entra" o "no entres" (solo educan)
- [ ] Tono amigable y personalizado al nivel del usuario
- [ ] Checklist visual aparece y es accionable
- [ ] Glosario funciona correctamente

---

### Fase 5: Feedback Loop & Refinamiento (Día 11-14)

**Frontend**
- [ ] Página PostSession (feedback post-salida)
- [ ] Botón "Salir del agua" en Landing
- [ ] Lógica de ajuste de perfil basado en feedback
- [ ] Implementar Service Worker (`sw.js`)
- [ ] Cache de assets estáticos
- [ ] Cache de último resultado (offline)
- [ ] Manifest.json con íconos
- [ ] Animaciones oceánicas
- [ ] Polish de UI/UX

**Backend**
- [ ] Endpoint `/api/feedback` para post-sesión
- [ ] Lógica de ajuste adaptativo (esfuerzo/disfrute, NO seguridad)
- [ ] Optimización de performance
- [ ] Rate limiting
- [ ] Logging

**Verificación Fase 5**
- [ ] Feedback post-sesión funciona
- [ ] Perfil se ajusta adaptivamente (esfuerzo/disfrute)
- [ ] Modelo de seguridad NUNCA se ajusta
- [ ] App instalable como PWA
- [ ] Funciona offline (muestra último resultado)
- [ ] Lighthouse score > 90
- [ ] Animaciones fluidas en móvil
