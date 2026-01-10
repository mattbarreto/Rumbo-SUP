# Rumbo SUP - PWA Móvil-First

Instructor virtual de Stand Up Paddle (SUP) para Mar del Plata, Argentina.

## 🎯 Arquitectura "Split Brain"

- **Layer A (Motor Determinístico)**: Calcula seguridad/esfuerzo/disfrute sin IA
- **Layer B (Pedagógico)**: IA explica las decisiones de forma educativa

**La IA nunca decide si entras o no. Solo enseña el "por qué".**

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
