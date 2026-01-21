# Rumbo SUP

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/backend-FastAPI-blue)
![React](https://img.shields.io/badge/frontend-React%20%2B%20Vite-61DAFB)
![License](https://img.shields.io/badge/license-MIT-green)

**Demo**: [rumbo.matiasbarreto.com](https://rumbo.matiasbarreto.com)

Rumbo SUP es una aplicación web progresiva (PWA) diseñada para practicantes de Stand Up Paddle en Mar del Plata. Combina datos meteorológicos en tiempo real con un motor de análisis híbrido para ofrecer recomendaciones personalizadas de seguridad y disfrute, adaptadas al nivel de experiencia del usuario.

---

## Arquitectura

El sistema utiliza una arquitectura "Split Brain" que separa las decisiones críticas de las explicaciones:

| Capa | Responsabilidad | Tecnología |
|------|-----------------|------------|
| **Layer A** (Determinístico) | Cálculo de scores de seguridad, esfuerzo y disfrute | Reglas Python |
| **Layer B** (Pedagógico) | Explicaciones educativas y contextuales | Google Gemini |

La IA nunca decide si el usuario entra al agua. Solo explica el "por qué" de cada recomendación.

### SenseiEngine

El motor de decisiones evalúa variables meteorológicas y genera flags semánticos:

| Condición | Flag | Impacto |
|-----------|------|---------|
| Tormenta eléctrica (WMO 95-99) | `tormenta_electrica` | Seguridad = 0 |
| Visibilidad < 1km | `visibilidad_nula` | Seguridad = 0 |
| Período < 5s | `mar_picado` | Esfuerzo +20 |
| UV > 6 | `uv_alto` | Alerta solar |
| Lluvia > 0.5mm | `lluvia` | Seguridad -10 |

---

## Características

- **Multi-Provider Resiliente**: Open-Meteo (principal), Windy.com (respaldo), OpenWeatherMap (fallback)
- **Smart Cache**: Persistencia inteligente en frontend para reducir latencia
- **Timeline Inteligente**: Proyección hora a hora con corrección de zona horaria
- **Análisis Semántico**: Traduce datos crudos en narrativas comprensibles
- **Sistema Responsive**: Garantiza estabilidad visual desde 320px hasta tablets
- **Animación de Viento**: Sistema de partículas con física avanzada (280 partículas, ~60 FPS)

---

## Stack Tecnológico

### Backend

- Python 3.10+ / FastAPI
- Patrón Provider para abstracción de fuentes de datos
- Cache inteligente (TTL 30min)
- Validación con Pydantic

### Frontend

- React 18 / Vite
- PWA con service worker
- Sistema de diseño basado en variables CSS (8pt grid, paleta oceánica)
- Animaciones con Canvas y Framer Motion

---

## Instalación

### Requisitos

- Python 3.10+
- Node.js 18+

### Backend

```bash
cd proyecto/backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

Crear archivo `.env` en `proyecto/backend/`:

```env
OPENWEATHER_API_KEY=tu_clave
WINDY_API_KEY=tu_clave
GEMINI_API_KEY=tu_clave
FRONTEND_URL=http://localhost:5173
```

Ejecutar:

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
cd proyecto/frontend
npm install
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`.

---

## Producción

| Servicio | URL |
|----------|-----|
| Frontend | `https://rumbo.matiasbarreto.com` |
| API | `https://rumbo-api.matiasbarreto.com` |

---

## APIs Utilizadas

| Proveedor | Uso | Documentación |
|-----------|-----|---------------|
| Open-Meteo | Datos marinos y atmosféricos (principal) | [Marine API](https://open-meteo.com/en/docs/marine-weather-api) |
| Windy.com | Respaldo de alta calidad | [Point Forecast API](https://api.windy.com/point-forecast/docs) |
| OpenWeatherMap | Fallback básico | [API Docs](https://openweathermap.org/api) |
| Google Gemini | Generación de explicaciones | `gemini-2.0-flash-exp` |

---

## Principios de Diseño

1. El semáforo indica seguridad, no "GO/NO-GO"
2. Decisión y explicación están separadas (Layer A vs Layer B)
3. El disfrute se calcula según el objetivo del usuario
4. El modelo de seguridad es inmutable

---

## Contribuir

Las contribuciones son bienvenidas. Antes de empezar:

1. Lee la [Guía de Contribución](docs/CONTRIBUTING.md)
2. Usa variables de entorno para claves API (nunca commitear credenciales)
3. Sigue [Conventional Commits](https://www.conventionalcommits.org/) para mensajes

Para reportar bugs o sugerir features, abrí un [issue](https://github.com/mattbarreto/rumbo-sup/issues).

---

## Licencia

MIT License. Ver [LICENSE](proyecto/LICENSE) para más detalles.

---

<p align="center">
  Desarrollado en Mar del Plata
</p>
