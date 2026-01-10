# Rumbo SUP - Deployment Guide

## Despliegue en Render.com

### Requisitos Previos
- Cuenta en [Render.com](https://render.com)
- Repositorio en GitHub con este código
- API Keys:
  - `GEMINI_API_KEY` (Google AI Studio)
  - `WORLDTIDES_API_KEY` (WorldTides API)

---

## Opción 1: Deploy Automático (Recomendado)

1. **Sube el código a GitHub**

2. **Conecta el repositorio a Render**
   - Ve a [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Selecciona tu repositorio
   - Render detectará `render.yaml` automáticamente

3. **Configura los secrets**
   En el dashboard de Render, configura:
   - `GEMINI_API_KEY` → Tu API key de Google
   - `WORLDTIDES_API_KEY` → Tu API key de WorldTides

4. **Deploy**
   - Click "Apply" para crear ambos servicios
   - Render se encarga del resto

---

## Opción 2: Deploy Manual

### Backend (Web Service)

1. **New Web Service** en Render
2. Configuración:
   - **Root Directory**: `proyecto/backend`
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**:
   ```
   GEMINI_API_KEY=<tu-key>
   WORLDTIDES_API_KEY=<tu-key>
   GEMINI_MODEL=gemini-2.0-flash-exp
   FRONTEND_URL=https://<tu-frontend>.onrender.com
   ```

### Frontend (Static Site)

1. **New Static Site** en Render
2. Configuración:
   - **Root Directory**: `proyecto/frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

3. **Environment Variables**:
   ```
   VITE_API_URL=https://<tu-backend>.onrender.com
   ```

4. **Rewrites** (para SPA routing):
   - Source: `/*`
   - Destination: `/index.html`

---

## Acceso a la App

La app está protegida con contraseña para beta testers:

**Password**: `supadmin`

Los usuarios deben ingresar esta contraseña la primera vez.
La sesión se guarda en localStorage.

---

## URLs de Producción

Una vez deployado, tendrás:
- **Frontend**: `https://rumbo-sup-frontend.onrender.com`
- **Backend API**: `https://rumbo-sup-api.onrender.com`
- **Docs API**: `https://rumbo-sup-api.onrender.com/docs`

---

## Notas Importantes

1. **Free Tier**: El servicio gratuito de Render "duerme" después de 15 min de inactividad. La primera request puede tardar ~30 segundos.

2. **API Keys**: Nunca commitees las API keys. Siempre configúralas en el dashboard de Render.

3. **CORS**: Ya está configurado para aceptar requests desde cualquier `.onrender.com` subdomain.
