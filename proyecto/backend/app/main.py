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
    """Root endpoint"""
    return {
        "message": "Rumbo SUP API",
        "version": "0.1.0",
        "docs": "/docs"
    }
