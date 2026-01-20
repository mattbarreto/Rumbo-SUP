from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import api
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear aplicación FastAPI
app = FastAPI(
    title="Rumbo SUP API",
    description="Backend para Rumbo SUP - Tu Guía de Mar",
    version="0.2.0"
)

# Configurar CORS para permitir frontend
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Detectar si estamos en producción o desarrollo
is_production = "onrender.com" in frontend_url

# Orígenes permitidos
allowed_origins = [
    frontend_url,
    "http://localhost:5173",      # Dev local
    "http://localhost:4173",      # Vite preview
]

# En producción, también permitir cualquier subdominio de Render
if is_production:
    allowed_origins.append("https://*.onrender.com")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.onrender\.com" if is_production else None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(api.router)

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    print("🌊 Rumbo SUP API iniciando...")
    print(f"📡 CORS configurado para: {frontend_url}")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre de la aplicación"""
    print("👋 Rumbo SUP API cerrando...")

@app.get("/")
async def root():
    """Root endpoint - Serves index.html if static files exist, else API info"""
    # Si existe el frontend build, servirlo
    if os.path.exists("app/static/index.html"):
        return FileResponse("app/static/index.html")
    return {
        "message": "Rumbo SUP API",
        "version": "0.2.0",
        "docs": "/docs",
        "status": "Frontend not mounted (check app/static)"
    }

# Servir archivos estáticos si existen (Producción)
# Se espera que el usuario copie 'frontend/dist' a 'backend/app/static'
if os.path.exists("app/static"):
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse
    
    # 1. Mount assets (JS/CSS)
    if os.path.exists("app/static/assets"):
        app.mount("/assets", StaticFiles(directory="app/static/assets"), name="assets")
        
    # 2. Otros archivos estáticos en root (favicon, manifesto, etc)
    # No montamos "/" directamente para no ocultar la API, lo manejamos manual o con excepciones
    
    # 3. SPA Catch-all (Para rutas de React como /login, /dashboard)
    # IMPORTANTE: Esto debe ir DESPUES de los routers de API
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Ignorar rutas de API (ya manejadas arriba)
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi"):
             from fastapi import HTTPException
             raise HTTPException(status_code=404, detail="Not Found")
        
        # Servir archivo si existe (ej: favicon.ico)
        file_path = os.path.join("app/static", full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
             return FileResponse(file_path)
             
        # Fallback a index.html para SPA routing
        return FileResponse("app/static/index.html")
