# 🌊 Rumbo SUP - Tu Guía de Mar Personal

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/backend-FastAPI-blue)
![React](https://img.shields.io/badge/frontend-React%20%2B%20Vite-61DAFB)
![License](https://img.shields.io/badge/license-MIT-green)

**Rumbo SUP** es una Aplicación Web Progresiva (PWA) diseñada para practicantes de Stand Up Paddle en Mar del Plata. Utiliza un motor híbrido de inteligencia meteorológica para analizar condiciones marítimas en tiempo real y ofrecer recomendaciones personalizadas de seguridad y disfrute, adaptadas a tu nivel de experiencia y equipamiento.

## 🚀 Características Principales

- **Sistema Multi-Provider Resiliente:** Arquitectura híbrida que consume datos de Stormglass (primario), OpenWeatherMap (secundario) y OpenMeteo (fallback), garantizando disponibilidad 24/7.
- **Análisis Semántico:** Transforma datos crudos (periodo de ola, nudos de viento) en narrativas comprensibles ("Mar picado", "Glassy", "Viento de tierra").
- **Personalización Contextual:** El motor de decisión (`SenseiEngine`) ajusta los scores de seguridad basándose en si tu tabla es rígida o inflable y tu experiencia previa.
- **Timeline Inteligente:** Proyección hora a hora con corrección automática de zona horaria y secuencia de datos.

## 🛠️ Arquitectura Técnica

El proyecto sigue una arquitectura desacoplada moderna:

### Backend (Python / FastAPI)
- **Providers Pattern:** Abstracción de fuentes de datos (`WeatherProvider` interface) permitiendo switch dinámico de APIs.
- **Hybrid Service:** Lógica de caché inteligente (TTL 30min) y orquestación de fallbacks.
- **Pydantic Models:** Validación estricta de datos para viento, olas y atmósfera.

### Frontend (React / Vite)
- **PWA First:** Diseñado para funcionar como app nativa en móviles.
- **Clean UI:** Interfaz minimalista enfocada en la legibilidad bajo luz solar directa.

## 🔌 APIs Integradas

| Provider | Rol | Datos | Estado |
|----------|-----|-------|--------|
| **Stormglass** | Primario | Olas, Viento, Marea | Limitado (10 req/día) |
| **OpenWeather**| Secundario| Clima, Viento, Temp | Alta disponibilidad |
| **OpenMeteo** | Fallback | Clima, Olas, UV | Gratuito ilimitado |

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
# Claves de API (Consíguelas en sus respectivos portales)
STORMGLASS_API_KEY=tu_clave_stormglass
OPENWEATHER_API_KEY=tu_clave_openweather
GEMINI_API_KEY=tu_clave_gemini (opcional, para features experimentales)

# Configuración
FRONTEND_URL=http://localhost:5173
```

### 2. Configuración del Frontend

```bash
cd proyecto/frontend
npm install
npm run dev
```

La app estará disponible en `http://localhost:5173`.

## 📦 Despliegue

La infraestructura está definida como código en `render.yaml`. El despliegue es automático en **Render.com** al hacer push a `main`.

**Variables de entorno requeridas en Producción:**
- `STORMGLASS_API_KEY`
- `OPENWEATHER_API_KEY`
- `GEMINI_API_KEY`
- `PYTHON_VERSION`: 3.11.6

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor, asegúrate de no subir archivos de configuración local o claves API. La carpeta `docs/` y los scripts de prueba (`test_*.py`) están ignorados por defecto.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

<p align="center">
  Hecho con 💙 y 🧉 en Mar del Plata
</p>
