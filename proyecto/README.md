# Rumbo SUP - PWA Móvil-First

Instructor virtual de Stand Up Paddle (SUP) para Mar del Plata, Argentina.

## 🎯 Arquitectura "Split Brain"

- **Layer A (Motor Determinístico)**: Calcula seguridad/esfuerzo/disfrute sin IA
- **Layer B (Pedagógico)**: IA explica las decisiones de forma educativa

**La IA nunca decide si entras o no. Solo enseña el "por qué".**

## 🧠 SenseiEngine (Motor de Decisiones)

El **SenseiEngine** es el núcleo determinístico que evalúa la seguridad y condiciones del mar. Se ha actualizado para procesar variables críticas de seguridad.

### Tabla de Variables y Flags

| Variable | Flag Generado | Impacto en Score | Impacto Semántico |
| :--- | :--- | :--- | :--- |
| **Tormenta (WMO 95-99)** | `tormenta_electrica` | **Seguridad = 0** (Bloqueante) | Alerta crítica de riesgo eléctrico. |
| **Visibilidad < 1km** | `visibilidad_nula` | **Seguridad = 0** | Aviso de desorientación. |
| **Periodo < 5s** | `mar_picado` | Esfuerzo +20 | Aviso de inestabilidad/equilibrio. |
| **UV Index > 6** | `uv_alto` | - | Consejos de protección solar. |
| **Lluvia > 0.5mm** | `lluvia` | Seguridad -10 | Aviso de frío/visibilidad. |

### Lógica de Puntuación
- **Seguridad (0-100)**: Inicia en 100. Resta por viento offshore (-15), lluvia (-10). Se vuelve 0 si hay tormenta eléctrica o visibilidad nula.
- **Esfuerzo (0-100)**: Suma basada en velocidad de viento y altura de ola. Se penaliza extra (+20) si el mar está "picado" (choppy), lo que requiere más corrección de postura.
- **Disfrute (0-100)**: Cálculo subjetivo basado en el objetivo del usuario (Calma vs Entrenamiento vs Desafío) y la calidad de la ola (periodo).

## 📡 Integración de APIs

El sistema utiliza un **HybridWeatherProvider** que orquesta múltiples fuentes de datos para obtener la mejor precisión y riqueza de variables.

### 1. Open-Meteo (Principal)
Proveedor primario para datos marinos y atmosféricos detallados.
- **Documentación**: [Open-Meteo Marine API](https://open-meteo.com/en/docs/marine-weather-api)
- **Variables Utilizadas**:
  - `wave_height`, `wave_period`, `wave_direction` (Olas)
  - `wind_speed_10m`, `wind_direction_10m`, `wind_gusts_10m` (Viento)
  - `uv_index`, `visibility`, `weathercode`, `precipitation` (Atmósfera)
- **Configuración**: Utilizamos el modelo `best_match` con coordenadas costeras exactas para evitar errores de interpolación en zonas de transición tierra-mar.

### 2. OpenWeatherMap (Respaldo)
Proveedor secundario para validación y fallback.
- **Documentación**: [OpenWeather API](https://openweathermap.org/api)
- **Uso**: Se utiliza si Open-Meteo falla, proveyendo datos básicos de viento y clima actual.

### 3. Google Gemini (IA Pedagógica)
Genera las explicaciones narrativas y consejos personalizados.
- **Modelo**: `gemini-2.0-flash-exp` (Optimizado para latencia baja).
- **Función**: Traduce los "Flags" y "Scores" del SenseiEngine en lenguaje natural y consejos de seguridad (e.g., "Usa lycra por UV alto").

## 🏗️ Stack Tecnológico

**Frontend**
- Vite + React (PWA móvil-first)
- Design system oceánico
- Service Workers para offline

**Backend**
- FastAPI (Python)
- Google Gemini (explicaciones pedagógicas)
- OpenMeteo Marine API (datos meteorológicos)

## 📁 Estructura

```
proyecto/
├── frontend/          # PWA móvil-first
├── backend/           # FastAPI
└── README.md
```

## 🚀 Quick Start

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🧪 Principios Arquitectónicos

1. **Semáforo = Solo seguridad** (nunca GO/NO-GO)
2. **Layer A y Layer B separados** (decisión vs explicación)
3. **Disfrute basado en objetivos** (calma/entrenamiento/desafío)
4. **Modelo de seguridad inmutable**

## 📝 Licencia

Proyecto educativo - No reemplaza juicio propio del usuario.
