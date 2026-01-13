# Rumbo SUP

Aplicación web progresiva (PWA) para practicantes de Stand Up Paddle en Mar del Plata. Consultá las condiciones del mar en tiempo real y recibí recomendaciones personalizadas según tu nivel y equipo.

## Qué hace

- Analiza viento, olas y marea en tiempo real
- Te dice si es buen momento para salir al agua
- Adapta las recomendaciones a tu experiencia y tipo de tabla

## Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** React + Vite (PWA)
- **APIs:** Stormglass (clima), OpenMeteo (fallback)
- **Deploy:** Render.com

## Instalación local

### Backend

```bash
cd proyecto/backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env     # Configurar API keys
python -m uvicorn app.main:app --reload
```

### Frontend

```bash
cd proyecto/frontend
npm install
npm run dev
```

Accedé a `http://localhost:5173` y listo.

## Variables de Entorno

Crear archivo `.env` en `proyecto/backend/`:

```
GEMINI_API_KEY=tu_key
STORMGLASS_API_KEY=tu_key
FRONTEND_URL=http://localhost:5173
```

## Deploy

El proyecto usa `render.yaml` para deploy automático. Configurá las variables de entorno en el dashboard de Render.

## Autor

Matías Barreto - [matiasbarreto.com](https://matiasbarreto.com/)

## Licencia

MIT
