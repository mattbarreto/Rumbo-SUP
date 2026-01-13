# 🏄 Rumbo SUP - Tu Guía de Mar Inteligente

![Rumbo SUP Banner](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge) ![Python](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge) ![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?style=for-the-badge) ![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange?style=for-the-badge) ![PWA](https://img.shields.io/badge/PWA-Mobile--First-blueviolet?style=for-the-badge)

**Rumbo SUP** es una **Progressive Web App (PWA)** móvil-first diseñada para practicantes de Stand Up Paddle en Mar del Plata. No es solo un pronóstico del clima; es un **instructor virtual con IA** que interpreta las condiciones (viento, olas, marea) basándose en tu nivel de experiencia y el tipo de tabla que usás.

> **100% Conforme con Mobile-First PWA Standards** - Diseñada con estética "Oceanic Minimalist" (Glassmorphism + Deep Ocean).

---

## 🌊 ¿Qué es Rumbo SUP?

Un asistente digital que combina:
- 📊 **Análisis determinístico** de condiciones de mar
- 🤖 **IA pedagógica** (Google Gemini) que explica el "por qué"
- 🎯 **Personalización** según tu tabla, nivel y objetivo

**Filosofía "Split Brain":**
- **Layer A (Risk Manager):** Motor matemático que calcula seguridad objetiva
- **Layer B (Sensei):** IA que traduce datos técnicos a experiencia sensorial

---

## ✨ Features

### Layer A - Safety Cockpit
- ✅ Análisis determinístico con métricas industriales
- ✅ Visualización de viento tipo Windy
- ✅ Timeline de pronóstico horario
- ✅ Algoritmo de "Disfrute" basado en objetivo de sesión
- ✅ Umbral de seguridad personalizado por nivel

### Layer B - Guía Pedagógico
- ✅ Explicaciones sensoriales con IA (Google Gemini 2.0)
- ✅ Contenido educativo con iconos oceánicos custom
- ✅ Tips de seguridad contextualizados
- ✅ Sistema de glosario interactivo

### PWA Features
- ✅ Installable como app nativa (iOS + Android)
- ✅ Funciona offline (Service Worker)
- ✅ Mobile-first con `100dvh` viewport
- ✅ Respeta safe-area-inset (notch de iPhone)
- ✅ Animaciones GPU-accelerated (60fps)
- ✅ Touch targets de 48x48px mínimo

### Integraciones
- 🌊 **OpenMeteo Marine API:** Datos de olas y viento en tiempo real
- 🌖 **WorldTides API:** Estado preciso de mareas
- 🤖 **Google Gemini 2.0:** Razonamiento pedagógico

---

## 🛠️ Tech Stack

### Frontend
- **React 18 + Vite** - Velocidad y modularidad
- **Framer Motion** - Animaciones physics-based
- **Custom CSS Design System** - Variables CSS (--ocean-*, --safety-*)
- **Tipografía Premium** - Outfit (display) + Inter (body)
- **Oceanic Icon System** - Iconos SVG conceptuales propios

### Backend
- **FastAPI (Python 3.11)** - API REST de alto rendimiento
- **Pydantic** - Validación estricta de datos
- **Uvicorn** - Servidor ASGI para producción

### Mobile-First PWA Standards
- ✅ `100dvh` viewport (no `100vh`)
- ✅ `safe-area-inset-*` respetado
- ✅ Solo animaciones de `transform` y `opacity`
- ✅ `text-wrap: balance` en headlines
- ✅ Touch targets mínimo 44x44px
- ✅ Sin bloqueo de paste en inputs

---

## 💻 Instalación Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/mattbarreto/Rumbo-SUP.git
cd Rumbo-SUP
```

### 2. Backend Setup

```bash
cd proyecto/backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar tus API keys:
# - GEMINI_API_KEY (obtener en https://makersuite.google.com/app/apikey)
# - WORLDTIDES_API_KEY (obtener en https://www.worldtides.info/developer)

# Iniciar servidor
python -m uvicorn app.main:app --reload
```

El backend estará disponible en `http://localhost:8000`

### 3. Frontend Setup

```bash
cd proyecto/frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

### 4. Acceder a la App

1. Abrí `http://localhost:5173` en tu navegador
2. Ingresá la contraseña de beta: **`supadmin`** (demo/testing password)
3. Completá el onboarding (tipo de tabla, nivel, objetivo)
4. ¡Explorá las condiciones del mar!

> **Nota sobre la contraseña:** El `PasswordGate` es solo para demo/beta. En producción se recomienda implementar autenticación real con JWT tokens o removerlo completamente.

---

## ☁️ Deploy en Render

El proyecto incluye un `render.yaml` (Blueprint) para deploy automático:

1. Conectá tu repo a [Render.com](https://render.com)
2. Creá un **Blueprint** desde el repositorio
3. Configurá las variables de entorno:
   - `GEMINI_API_KEY`
   - `WORLDTIDES_API_KEY`
   - `FRONTEND_URL` (URL del frontend en Render)
   - `VITE_API_URL` (URL del backend en Render)
4. Render levantará automáticamente:
   - Backend (Web Service en Python)
   - Frontend (Static Site)

**Arquitectura en Render:**
- Backend: Free Web Service (Python)
- Frontend: Free Static Site
- Ambos servicios se comunican via CORS configurado

---

## 📱 Uso Móvil

### Instalación como PWA

**iOS (Safari):**
1. Abrí la web en Safari
2. Tap en el botón "Compartir"
3. Seleccioná "Agregar a pantalla de inicio"
4. La app se instalará como nativa

**Android (Chrome):**
1. Abrí la web en Chrome
2. Tap en el menú (⋮)
3. Seleccioná "Instalar app"
4. Confirmá la instalación

### Funcionalidad Offline

Gracias al Service Worker, la app funciona parcialmente offline:
- ✅ UI y diseño se cargan offline
- ✅ Última data consultada se cachea
- ⚠️ Datos en tiempo real requieren conexión

---

## 🏗️ Arquitectura del Proyecto

```
Rumbo-SUP/
├── proyecto/
│   ├── backend/              # FastAPI Backend
│   │   ├── app/
│   │   │   ├── engine/       # Layer A - Motor determinístico
│   │   │   ├── services/     # Integraciones (OpenMeteo, WorldTides, Gemini)
│   │   │   ├── routers/      # Endpoints de API
│   │   │   └── models/       # Schemas Pydantic
│   │   ├── requirements.txt
│   │   └── .env.example      # Template de variables de entorno
│   │
│   └── frontend/             # React + Vite Frontend
│       ├── src/
│       │   ├── components/   # Componentes React
│       │   ├── services/     # API client
│       │   ├── hooks/        # Custom hooks
│       │   ├── index.css     # Design system
│       │   └── fonts.css     # Tipografía
│       ├── public/
│       │   ├── manifest.json # PWA manifest
│       │   └── icons/        # App icons
│       └── vite.config.js    # Vite + PWA config
│
├── render.yaml               # Render deployment blueprint
├── README.md                 # Este archivo
└── .gitignore
```

---

## 🎨 Design System "Oceanic Minimalist"

### Filosofía
- **Core Feeling:** Calm, rhythmic, deep, organic
- **Metaphor:** Interface mimics the ocean - from "Abyss" background to "Surface" accents
- **Motion:** Animations "breathe" (4s cycle) or "flow" like waves (6s cycle)

### Color Palette
| Token | Hex | Usage |
|-------|-----|-------|
| `ocean.abyss` | `#0A1628` | Main background |
| `ocean.shimmer` | `#61A5C2` | Primary brand color |
| `ocean.foam` | `#A9D6E5` | Subtle accents |
| `ocean.sand` | `#F5F1EB` | Primary text |

### Typography
- **Display:** Outfit (geométrica, bold)
- **Body:** Inter (legibilidad universal)
- **Scale:** Golden Ratio (~1.618×)

### Components
- Glass cards con glassmorphism
- Breathing ring indicator (pulsing)
- Wind visualizer (particle system)
- Timeline widget (scrollable forecast)

Ver detalles completos en [`design_system.md`](design_system.md)

---

## 🔒 Seguridad y Best Practices

### Variables de Entorno
**Nunca commitees** el archivo `.env` al repositorio. Siempre usá `.env.example` como template.

```env
# .env.example
GEMINI_API_KEY=your_gemini_api_key_here
WORLDTIDES_API_KEY=your_worldtides_api_key_here
```

### Contraseña de Demo
La contraseña `supadmin` en `PasswordGate.jsx` es **solo para demo/beta**. Para producción:
- Opción 1: Remover el componente completamente
- Opción 2: Implementar autenticación real con JWT tokens en FastAPI

### CORS
El backend está configurado para aceptar requests solo desde el frontend en desarrollo y producción:
```python
origins = [
    "http://localhost:5173",  # Dev
    os.getenv("FRONTEND_URL")  # Production
]
```

---

## 📊 Testing

### Backend Tests
```bash
cd proyecto/backend
pytest
```

### Frontend Tests
```bash
cd proyecto/frontend
npm run test
```

### Mobile Testing
1. Usá Chrome DevTools en modo móvil
2. Probá en dispositivo físico para safe-area-inset
3. Verificá funcionamiento de PWA install prompt

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Creá una branch para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abrí un Pull Request

---

## 📝 Roadmap

- [ ] Multi-spot support (otros puntos de Mar del Plata)
- [ ] Auto-detección de spot por geolocalización
- [ ] Historial de sesiones
- [ ] Feedback loop adaptativo
- [ ] Notificaciones push cuando condiciones son ideales
- [ ] Modo oscuro/claro toggle
- [ ] Soporte multi-idioma (EN/ES)
- [ ] Expansión a otras ciudades costeras

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 👤 Autor

**Matías Barreto**  
Creative Technologist & AI Designer

- Website: [matiasbarreto.com](https://matiasbarreto.com/)
- LinkedIn: [@matiasbarreto](https://www.linkedin.com/in/matiasbarreto/)
- GitHub: [@mattbarreto](https://github.com/mattbarreto)

---

## 🙏 Agradecimientos

- **Google Gemini** - IA pedagógica
- **OpenMeteo** - Datos meteorológicos gratuitos y open-source
- **WorldTides** - Datos precisos de mareas
- **Render** - Hosting y deployment

---

Desarrollado con 💙 y 🌊 para la comunidad de SUP en Mar del Plata.
