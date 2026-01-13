# Rumbo SUP

Aplicación web para practicantes de Stand Up Paddle en Mar del Plata. Analiza condiciones del mar (viento, olas, marea) y ofrece recomendaciones personalizadas según tu nivel y equipo.

## Tecnologías

**Backend:** FastAPI (Python 3.11)  
**Frontend:** React + Vite  
**Deploy:** Render.com  

## Instalación

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

## Variables de Entorno

Crear archivo `.env` en `proyecto/backend/` con:

```
GEMINI_API_KEY=...
STORMGLASS_API_KEY=...
FRONTEND_URL=http://localhost:5173
```

## Deploy

El proyecto incluye `render.yaml` para deploy automático en Render.com. Configurar las variables de entorno en el dashboard de Render.

## Estructura

```
proyecto/
├── backend/          # API FastAPI
│   └── app/
│       ├── routers/  # Endpoints
│       ├── services/ # Providers (Stormglass, OpenMeteo)
│       └── models/   # Schemas Pydantic
└── frontend/         # React PWA
    └── src/
        └── components/
```

## Licencia

MIT

## Autor

Matías Barreto - [matiasbarreto.com](https://matiasbarreto.com/)
