# 🏄 Rumbo SUP - Tu Guía de Mar

![Rumbo SUP Banner](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge) ![Python](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge) ![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?style=for-the-badge) ![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange?style=for-the-badge)

Rumbo SUP es una **Progressive Web App (PWA)** diseñada para practicantes de Stand Up Paddle en Mar del Plata. No es solo un pronóstico del clima; es un **instructor virtual** que interpreta las condiciones (viento, olas, marea) basándose en tu nivel de experiencia y el tipo de tabla que usás.

> **Experiencia Premium**: Diseñada con una estética "Deep Ocean" (Glassmorphism + Dark Mode) y arquitectura mobile-first.

---

## 🧠 Arquitectura "Split Brain"

Este proyecto utiliza una arquitectura de doble capa para garantizar seguridad y pedagogía:

1.  **Layer A (Determinístico - El "Risk Manager")**:
    *   **Motor Matemático**: Calcula scores de seguridad (0-100) basándose estrictamente en datos físicos (viento, ráfagas, olas).
    *   **Inmutable**: No usa IA. Si el viento supera 30km/h, es bandera roja. Punto.
    *   **Personalizado**: Ajusta los umbrales según si sos Principiante, Intermedio o Avanzado.

2.  **Layer B (Pedagógico - El "Sensei")**:
    *   **IA Generativa (Google Gemini)**: Recibe los datos del Layer A y los "traduce" a una explicación humana.
    *   **Enfoque Sensorial**: No te dice "Viento 15 nudos". Te dice *"Vas a sentir una brisa fresca en la cara, y el mar tendrá una textura rugosa pero navegable"*.
    *   **Prohibición de Decisión**: La IA tiene prohibido explícitamente tomar decisiones de seguridad (Go/No-Go). Solo explica y enseña.

---

## 🚀 Features

*   **Safety Cockpit (Layer A):** Análisis determinístico con métricas industriales - números grandes, alto contraste, optimizado para luz solar y manos mojadas.
*   **Guía del Mar (Layer B):** Explicación pedagógica con IA (Google Gemini 2.0) que traduce datos técnicos a experiencia sensorial.
*   **Algoritmo de Disfrute**: Calcula no solo si es seguro, sino si vas a pasarla bien según tu objetivo (Calma, Entreno o Desafío).
*   **Gestión de Perfiles**: Ajusta las recomendaciones según tu tabla (Inflable vs. Rígida), nivel y potencia de remada.
*   **Integraciones Reales**:
    *   🌊 **OpenMeteo Marine API**: Datos de olas y viento en tiempo real.
    *   🌖 **WorldTides API**: Estado preciso de las mareas localizadas.
    *   🤖 **Google Gemini 2.0**: Capa de razonamiento pedagógico.
*   **PWA Installable**: Funciona como una app nativa en iOS y Android.
*   **Oceanic Utility Design:** Thumb Zone de 56px, botones sin diagonales, texto negro sobre colores de seguridad para máxima visibilidad solar.

---

## 🛠️ Tech Stack

### Frontend
- **React 18 + Vite**: Velocidad y modularidad.
- **Framer Motion**: Animaciones physics-based suaves.
- **Custom CSS Design System**: Variables CSS (--ocean-*, --safety-*), Glassmorphism, sin frameworks pesados.
- **Tipografía Premium**: Outfit (display/geométrica) + Inter (body/legibilidad universal).
- **Oceanic Icon System**: Iconos SVG conceptuales propios con metáforas oceánicas (horizonte, olas, navegación).

### Backend
- **FastAPI (Python 3.11)**: API REST de alto rendimiento.
- **Pydantic**: Validación estricta de datos.
- **Uvicorn**: Servidor ASGI para producción.

---

## 💻 Instalación Local

1.  **Clonar el repo**
    ```bash
    git clone https://github.com/mattbarreto/Rumbo-SUP.git
    cd Rumbo-SUP
    ```

2.  **Backend**
    ```bash
    cd proyecto/backend
    python -m venv venv
    source venv/bin/activate  # o .\venv\Scripts\activate en Windows
    pip install -r requirements.txt
    
    # Crear .env basado en .env.example
    cp .env.example .env
    # Completar API Keys (Gemini y WorldTides)
    
    python -m uvicorn app.main:app --reload
    ```

3.  **Frontend**
    ```bash
    cd proyecto/frontend
    npm install
    npm run dev
    ```

---

## ☁️ Deploy (Render)

El proyecto incluye un `render.yaml` (Blueprint) para deploy automático.

1.  Conectá tu repo a [Render.com](https://render.com).
2.  Creá un **Blueprint**.
3.  Seteá las variables de entorno (`GEMINI_API_KEY`, `WORLDTIDES_API_KEY`).
4.  ¡Listo! Render levantará el Backend (Python) y el Frontend (Static) automáticamente.

---

Desarrollado con 💙 y 🧉 para la comunidad de SUP.
