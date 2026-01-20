# 🌊 Rumbo SUP - Tu Guía de Mar Personal

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/backend-FastAPI-blue)
![React](https://img.shields.io/badge/frontend-React%20%2B%20Vite-61DAFB)
![License](https://img.shields.io/badge/license-MIT-green)

🔗 **Demo en vivo**: [rumbo.matiasbarreto.com](https://rumbo.matiasbarreto.com)

**Rumbo SUP** es una Aplicación Web Progresiva (PWA) diseñada para practicantes de Stand Up Paddle en Mar del Plata. Utiliza un motor híbrido de inteligencia meteorológica para analizar condiciones marítimas en tiempo real y ofrecer recomendaciones personalizadas de seguridad y disfrute, adaptadas a tu nivel de experiencia y equipamiento.

## 🎯 Arquitectura "Split Brain"

- **Layer A (Motor Determinístico)**: Calcula seguridad/esfuerzo/disfrute sin IA. Riguroso y predecible.
- **Layer B (Pedagógico)**: IA (Google Gemini) explica las decisiones de forma educativa y empática.

**La IA nunca decide si entras o no. Solo enseña el "por qué".**

## 🧠 SenseiEngine (Motor de Decisiones)

El **SenseiEngine** es el núcleo determinístico que evalúa la seguridad y condiciones del mar. Se encarga de traducir variables crudas en semántica de surf.

### Variables Críticas y Flags

| Variable | Flag Generado | Impacto en Score | Impacto Semántico |
| :--- | :--- | :--- | :--- |
| **Tormenta (WMO 95-99)** | `tormenta_electrica` | **Seguridad = 0** (Bloqueante) | Alerta crítica de riesgo eléctrico. |
| **Visibilidad < 1km** | `visibilidad_nula` | **Seguridad = 0** | Aviso de desorientación. |
| **Periodo < 5s** | `mar_picado` | Esfuerzo +20 | Aviso de inestabilidad/equilibrio. |
| **UV Index > 6** | `uv_alto` | - | Consejos de protección solar. |
| **Lluvia > 0.5mm** | `lluvia` | Seguridad -10 | Aviso de frío/visibilidad. |

### Lógica de Puntuación
- **Seguridad (0-100)**: Inicia en 100. Resta por viento offshore (-15), lluvia (-10). Se vuelve 0 si hay tormenta eléctrica o visibilidad nula.
- **Esfuerzo (0-100)**: Suma basada en velocidad de viento y altura de ola. Se penaliza extra (+20) si el mar está "picado" (choppy).
- **Disfrute (0-100)**: Cálculo subjetivo basado en el objetivo del usuario (Calma vs Entrenamiento vs Desafío).

## 🚀 Características Principales

- **Sistema Multi-Provider Resiliente:** Arquitectura híbrida que consume datos de Open-Meteo (primario), Windy.com (respaldo de élite) y OpenWeatherMap (último recurso).
- **Smart Session Cache:** Persistencia inteligente en frontend para reducir latencia y consumorojo de API.
- **Auditoría Forense:** Herramienta de autodiagnóstico (`/api/audit`) para verificar la salud de todos los proveedores en tiempo real.
- **Análisis Semántico:** Transforma datos crudos en narrativas comprensibles ("Mar picado", "Glassy", "Viento de tierra").
- **Personalización Contextual:** Ajusta scores basándose en tabla (rígida/inflable) y experiencia.
- **Timeline Inteligente:** Proyección hora a hora con corrección automática de zona horaria.

### 🎨 Animación de Viento Elite (Nuevo)

Sistema de partículas de nivel AAA con **9 features de física avanzada**:

1. **Depth Layering**: 3 capas parallax para efecto 3D (fondo 30%, medio 60%, frente 100%)
2. **Wind Gusts**: Ráfagas periódicas que simulan la respiración natural del aire
3. **Multi-Frequency Turbulence**: 3 ondas sinusoidales combinadas para movimiento orgánico
4. **Fade Lifecycle**: Spawn/despawn cinematográfico de partículas
5. **Clustering**: Agrupaciones emergentes (atracción entre partículas 10-50px)
6. **Wind Wake**: 🌟 **Interacción táctil** - Las partículas se apartan al tocar/arrastrar
7. **Smart Respawn**: Reposicionamiento inteligente basado en dirección de flujo
8. **Layer-Specific Colors**: Opacidades diferenciadas por profundidad
9. **Perpendicular Turbulence**: Desplazamiento transversal al flujo para realismo

**Performance**: 280 partículas optimizadas, ~60 FPS en dispositivos modernos.

## 📡 Integración de APIs

El sistema utiliza un **HybridWeatherProvider** que orquesta múltiples fuentes:

### 1. Open-Meteo (Principal)
Proveedor primario para datos marinos y atmosféricos.
- **Documentación**: [Open-Meteo Marine API](https://open-meteo.com/en/docs/marine-weather-api)
- **Uso**: Modelo `best_match` con coordenadas costeras exactas para evitar errores de interpolación tierra-mar.

### 2. Windy.com (Respaldo de Élite)
Se activa automáticamente si Open-Meteo falla (Error 429/503).
- **Documentación**: [Windy Point Forecast API v2](https://api.windy.com/point-forecast/docs)
- **Uso**: Modelos `gfs` (viento) y `gfsWave` (olas).
- **Ventaja**: Datos de altísima calidad y fiabilidad comercial.

### 3. OpenWeatherMap (Último Recurso)
Fallback final para validación básica.
- **Documentación**: [OpenWeather API](https://openweathermap.org/api)
- **Uso**: Datos básicos de viento y clima si fallan los anteriores.

### 4. Google Gemini (IA Pedagógica)
Genera las explicaciones narrativas.
- **Modelo**: `gemini-2.0-flash-exp`.
- **Uso**: Traduce Flags y Scores en consejos de seguridad ("Usa lycra", "Cuidado con la deriva").

## 🛠️ Arquitectura Técnica

### Backend (Python / FastAPI)
- **Providers Pattern:** Abstracción de fuentes de datos (`WeatherProvider` interface).
- **Hybrid Service:** Lógica de caché inteligente (TTL 30min) y orquestación de fallbacks.
- **Pydantic Models:** Validación estricta de datos.
- **Scoring System:** Sistema multidimensional (Seguridad/Esfuerzo/Disfrute) con reglas determinísticas.

### Frontend (React / Vite)
- **PWA First:** Diseñado para funcionar como app nativa en móviles.
- **Design System Orgánico:** Sistema completo de variables CSS (8 tamaños de border-radius, 8pt grid spacing, paleta oceánica).
- **Elite Animations:** Canvas-based particle system con física avanzada.
- **Componentes Modulares**: Arquitectura componentizada con separación clara de responsabilidades.

📚 **Documentación detallada**: Ver [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) para diagramas y explicación profunda del sistema (solo en repo local).

## ⚙️ Instalación Local

### Prerrequisitos
- Python 3.10+
- Node.js 18+

### 1. Configuración del Backend

```bash
cd proyecto/backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

Crea un archivo `.env` en `proyecto/backend/` con tus credenciales:

```env
OPENWEATHER_API_KEY=tu_clave
WINDY_API_KEY=tu_clave_windy
GEMINI_API_KEY=tu_clave
FRONTEND_URL=http://localhost:5173
```

### 2. Configuración del Frontend

```bash
cd proyecto/frontend
npm install
npm run dev
```

La app estará disponible en `http://localhost:5173`.

## 📦 Demo en Producción

| Servicio | URL |
|----------|-----|
| Frontend | `https://rumbo.matiasbarreto.com` |
| Backend API | `https://rumbo-api.matiasbarreto.com` |

## 🧪 Principios Arquitectónicos

1. **Semáforo = Solo seguridad** (nunca GO/NO-GO).
2. **Layer A y Layer B separados** (decisión vs explicación).
3. **Disfrute basado en objetivos** (calma/entrenamiento/desafío).
4. **Modelo de seguridad inmutable**.

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Lee la [Guía de Contribución](docs/CONTRIBUTING.md) para code style y workflow (solo en repo local)
2. No subas claves API - usa variables de entorno
3. Sigue [Conventional Commits](https://www.conventionalcommits.org/) para mensajes

**Issues**: [GitHub Issues](https://github.com/tuusuario/rumbo-sup/issues)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

<p align="center">
  Hecho con 💙 y 🧉 en Mar del Plata
</p>
