# 📊 Rumbo SUP - Abstracción del Proyecto Actual

## 🎯 Propósito del Proyecto Original

**SUP Sensei** es un instructor virtual para Stand Up Paddle (SUP) que ayuda a los usuarios a decidir si es seguro entrar al agua basándose en condiciones meteorológicas y oceanográficas en tiempo real.

### Filosofía "Split Brain"

- **Layer A (Cerebro Lógico)**: Motor determinístico que calcula el riesgo SIN IA - resultados reproducibles y transparentes
- **Layer B (Cerebro Pedagógico)**: IA (Google Gemini) que **explica** las decisiones de forma educativa, nunca decide por sí misma

> **Principio clave**: La IA nunca decide si entras o no. Solo enseña el "por qué".

---

## 🏗️ Arquitectura Técnica Actual

### Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Frontend | React Native (Expo) |
| Backend | Python FastAPI |
| Datos Meteorológicos | OpenMeteo Marine API |
| LLM | Google Gemini |
| Design System | Custom "Ocean" theme |

### Estructura Backend

```
/backend/app
├── /api              # Endpoints FastAPI
│   ├── routes.py     # Motor de análisis
│   ├── pedagogy.py   # Explicaciones IA
│   └── health.py     # Health check
├── /engine           # Motor determinístico (Layer A)
│   └── rules.py      # SenseiEngine - lógica de riesgo
├── /pedagogy         # Cliente Gemini (Layer B)
│   ├── llm_client.py
│   ├── prompts.py
│   └── glossary.py
├── /services         # Integración OpenMeteo
│   └── weather_service.py
└── /models           # Schemas Pydantic
    ├── weather.py
    ├── spot.py
    ├── user.py
    └── engine.py
```

### Estructura Frontend

```
/frontend/src
├── /features
│   ├── /gonogo       # Pantalla principal - indicador Go/No-Go
│   ├── /sensei       # Explicaciones educativas (IA)
│   └── /profile      # Onboarding de usuario
├── /components       # UI components reutilizables
└── /theme            # Design tokens (colores, animaciones)
```

---

## 🧠 Lógica de Negocio Core

### 1. Motor Determinístico (`SenseiEngine`)

**Responsabilidad**: Calcular riesgo, esfuerzo y disfrute basándose en:
- Condiciones meteorológicas actuales
- Características del spot (ubicación)
- Perfil del usuario

#### Inputs del Motor

**a) Datos Meteorológicos (`WeatherData`)**
- Viento: velocidad (km/h), dirección (grados)
- Olas: altura (metros)
- Mareas: estado (subiendo/bajando)

**b) Datos del Spot (`SpotData`)**
- Nombre y ubicación
- Orientación de la costa (grados) - para calcular viento onshore/offshore
- Reglas específicas del lugar (e.g., "marea bajando + viento offshore = deriva peligrosa")

**c) Perfil de Usuario (`UserProfile`)**
- Tipo de tabla: rígida/inflable
- Nivel de experiencia: principiante/intermedio/avanzado
- Potencia de remada: baja/media/alta

#### Outputs del Motor (`EngineResult`)

**Scores Numéricos (0-100)**
- `riesgo`: nivel de peligro
- `esfuerzo`: dificultad física esperada
- `disfrute`: diversión proyectada

**Categorías Cualitativas**
- `riesgo`: bajo/medio/alto
- `esfuerzo`: bajo/medio/alto
- `disfrute`: bajo/medio/alto

**Flags de Alerta**
- `viento_fuerte`: si viento > 30 km/h
- `riesgo_deriva`: tabla inflable + viento offshore
- Flags custom por spot

**Confianza del Modelo**
- `alta/media/baja` según completitud de datos

#### Algoritmo de Evaluación

1. **Contextualización**: Calcula dirección relativa del viento (onshore/offshore/cross-shore)
2. **Evaluación de Reglas Base**: Chequea condiciones peligrosas universales
3. **Reglas Específicas del Spot**: Evalúa condiciones custom del lugar
4. **Cálculo de Scores**: Combina flags y valores crudos en puntuaciones
5. **Categorización**: Convierte scores numéricos en labels (bajo/medio/alto)

### 2. Sistema Pedagógico (Layer B)

**Responsabilidad**: Generar explicaciones educativas basadas en el `EngineResult`

#### Proceso

1. Frontend envía resultado del motor a `/api/v1/pedagogy/explain`
2. Backend construye prompt estructurado para Gemini con:
   - Contexto del usuario (experiencia, tabla)
   - Condiciones actuales
   - Scores y flags del motor
   - Glosario de términos técnicos
3. Gemini retorna explicación en lenguaje natural
4. Frontend muestra en la pantalla "Sensei"

#### Características de las Explicaciones

- Tono: Educativo, amigable, no alarmista
- Estructura: Por qué es así, qué significa cada factor, tips de seguridad
- Personalización: Adaptada al nivel del usuario

---

## 📱 Flujo de Usuario Actual

### 1. Onboarding (Pantalla Profile)
- Usuario selecciona tipo de tabla
- Indica nivel de experiencia
- Configura potencia de remada
- (Guardado en estado local - no persiste actualmente)

### 2. Pantalla Go/No-Go (Principal)
- Muestra indicador visual de riesgo
- Scores de riesgo/esfuerzo/disfrute
- Botón "¿Por qué?" para modo Sensei
- UI oceánica con animaciones

### 3. Pantalla Sensei (Explicaciones)
- Texto generado por IA explicando las condiciones
- Contexto educativo sobre seguridad en SUP
- Links a glosario de términos

---

## 🌊 Datos y Modelos

### Modelo de Datos Meteorológicos

```python
WeatherData:
  wind:
    speed_kmh: float
    direction_deg: int (0-360, 0=North)
  waves:
    height_m: float
  tide:
    state: TideState (rising/falling)
```

### Modelo de Spot (Ubicación)

```python
SpotData:
  nombre: str
  lat: float
  lon: float
  orientation_costa_deg: int  # Dirección que mira la costa
  reglas_especificas: List[Rule]
```

**Ejemplo de Regla Específica**:
```python
Rule:
  condition: "tide_state == 'falling' and wind_dir_rel == 'offshore'"
  flag: "riesgo_deriva"
  descripcion: "Marea bajando con viento offshore puede alejarte"
```

### Modelo de Usuario

```python
UserProfile:
  board_type: BoardType (rigid/inflatable)
  experience: ExperienceLevel (beginner/intermediate/advanced)
  paddle_power: PaddlePower (low/medium/high)
```

---

## 🎨 UI/UX Actual

### Design System "Ocean"

**Paleta de Colores**
- Azules profundos y cyan para ambiente oceánico
- Gradientes de agua
- Alertas en naranja/rojo para riesgos

**Animaciones**
- Olas animadas en fondo
- Transiciones suaves
- Efectos de glassmorphism

**Componentes**
- Indicador circular de riesgo
- Cards para métricas
- Botones con estados visuales claros

---

## 🔧 Integraciones Externas

### OpenMeteo Marine API
- **Endpoint**: `https://marine-api.open-meteo.com/v1/marine`
- **Parámetros**: lat, lon, variables (wave_height, wind_speed, etc.)
- **Respuesta**: JSON con series temporales horarias
- **Estado actual**: Configurado pero no en producción (usando datos mock)

### Google Gemini
- **Modelo**: `gemini-2.0-flash-exp`
- **Input**: Prompt estructurado con contexto + engine result
- **Output**: Texto markdown con explicación
- **Estado actual**: Implementado y testeable

---

## 🚀 Estado del Proyecto

### ✅ Implementado
- Motor determinístico completo
- API FastAPI funcional
- Frontend React Native con UI oceánica
- Pantallas Go/No-Go, Sensei, Profile
- Integración Gemini (Layer B)
- Datos mock para testing

### ⚠️ Pendiente
- Conexión real a OpenMeteo
- Persistencia de perfil de usuario
- Múltiples spots de Mar del Plata
- Notificaciones push
- Historial de sesiones
- Builds para iOS/Android

### 🐛 Problemas Conocidos
- Error de bundling en frontend (`babel-preset-expo`)
- Falta validación robusta de reglas específicas
- Sistema de evaluación de reglas usa `eval()` (riesgo de seguridad)

---

## 💡 Insights para la Re-Implementación

### Fortalezas a Mantener
1. **Separación clara**: Layer A (lógica) vs Layer B (pedagogía)
2. **Transparencia**: El motor es determinístico y auditable
3. **Escalabilidad**: Fácil agregar nuevos spots con reglas custom
4. **Educación**: Enfoque en enseñar, no solo alertar

### Oportunidades de Mejora
1. **Stack más ligero**: React Native + Expo puede ser pesado para MVP
2. **PWA móvil**: Web app con acceso a geolocalización
3. **Despliegue ágil**: Sin necesidad de App Store/Play Store
4. **Testing más rápido**: Hotreloading en navegador móvil
5. **Backend simplificado**: Considerar API serverless o edge functions

### Requisitos Nuevos
1. **Geolocalización obligatoria**: Solo funciona en móviles con GPS
2. **Enfoque geográfico**: Priorizar Mar del Plata (Varese + otros spots)
3. **Multi-spot**: Detectar automáticamente el spot más cercano
4. **SaaS approach**: Arquitectura para múltiples ciudades futuras

---

## 🌍 Contexto Geográfico

### Mar del Plata - Spots Principales

**Varese**
- Playa protegida al norte de MDQ
- Viento predominante del SE
- Ideal para principiantes

**Otros spots a considerar**:
- Punta Mogotes
- La Perla
- Playa Grande
- Waikiki

### Condiciones Típicas
- Vientos: Variables, predominancia SE
- Olas: Moderadas (0.5-2m típicamente)
- Mareas: Semi-diurnas (2 altas/día)

---

## 🎯 Objetivo del Re-Diseño

Crear una **Progressive Web App (PWA)** móvil-first que:
- Sea más ágil de desarrollar e iterar
- Funcione solo en dispositivos móviles con GPS
- Detecte automáticamente el spot más cercano
- Mantenga la filosofía Split Brain
- Pueda escalar a otras ciudades costeras
- Sea fácil de testear localmente en Mar del Plata
