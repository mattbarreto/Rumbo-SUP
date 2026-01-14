# 🏄 Rumbo SUP - Prompt para Nuevo Contexto

## 📋 Resumen Ejecutivo

Necesito crear **Rumbo SUP**, una Progressive Web App (PWA) móvil-first que funcione como instructor virtual para practicantes de Stand Up Paddle (SUP) en Mar del Plata, Argentina.

La aplicación debe ayudar a decidir si es seguro entrar al agua basándose en condiciones meteorológicas y oceanográficas en tiempo real, siguiendo una arquitectura "Split Brain" donde:
- **Layer A (Lógico)**: Motor determinístico que calcula riesgo SIN IA
- **Layer B (Pedagógico)**: IA que explica las decisiones de forma educativa

**La IA nunca decide si entras o no. Solo enseña el "por qué".**

---

## 🎯 Objetivos del Proyecto

### Objetivo Principal
Crear una web app que solo funcione en dispositivos móviles con GPS, detecte automáticamente el spot de SUP más cercano en Mar del Plata, y proporcione:
1. Análisis de riesgo/esfuerzo/disfrute basado en condiciones meteorológicas
2. Explicaciones educativas generadas por IA
3. Recomendaciones de seguridad personalizadas

### Objetivos Secundarios
- Arquitectura escalable para agregar más ciudades costeras en el futuro (modelo SaaS)
- Desarrollo e iteración ágiles
- Testing fácil en el terreno (Mar del Plata)
- Deploy rápido sin depender de App Stores

---

## 🌍 Contexto Geográfico

### Mar del Plata - Spots de SUP

**Varese** (Spot prioritario)
- Ubicación: Zona norte de Mar del Plata
- Coordenadas aproximadas: -37.9833° S, -57.5333° W
- Características: Playa protegida, ideal para principiantes
- Viento predominante: SE

**Otros Spots** (fase futura)
- Punta Mogotes
- La Perla
- Playa Grande
- Waikiki

### Condiciones Meteorológicas Típicas
- Vientos: Variables, predominancia del SE, ráfagas en verano
- Olas: Moderadas (0.5-2m típicamente)
- Mareas: Semi-diurnas (2 altas y 2 bajas por día)
- Temporada: SUP practicable todo el año, pico en Nov-Mar

---

## 👥 Usuarios Objetivo

### Perfil Principal
- Practicantes de SUP en Mar del Plata
- Nivel: Principiante a Intermedio (principalmente)
- Necesidad: Tomar decisiones informadas sobre seguridad

### Datos del Usuario a Capturar
1. **Tipo de tabla**
   - Rígida (mejor performance, más estable)
   - Inflable (más portable, pero deriva más con viento)

2. **Nivel de experiencia**
   - Principiante: <10 salidas o <6 meses
   - Intermedio: 10-50 salidas o 6-24 meses
   - Avanzado: >50 salidas o >2 años

3. **Potencia de remada**
   - Baja: se cansa rápido, dificultad contra viento
   - Media: resistencia moderada
   - Alta: puede remar contra viento sostenido

---

## 🧠 Lógica de Negocio Core

### Motor Determinístico (Layer A)

#### Inputs
1. **Datos Meteorológicos** (de OpenMeteo Marine API)
   - Velocidad del viento (km/h)
   - Dirección del viento (grados, 0=Norte)
   - Altura de olas (metros)
   - Estado de marea (subiendo/bajando)

2. **Datos del Spot**
   - Ubicación (lat, lon)
   - Orientación de costa (grados) - para calcular viento relativo
   - Reglas específicas del lugar

3. **Perfil de Usuario**
   - Tipo de tabla, experiencia, potencia de remada

#### Outputs
**Scores Numéricos (0-100)**
- `riesgo`: peligro estimado
- `esfuerzo`: dificultad física
- `disfrute`: diversión proyectada

**Categorías** 
- Cada score se traduce a: `bajo` / `medio` / `alto`

**Flags de Alerta**
- `viento_fuerte`: viento > 30 km/h
- `riesgo_deriva`: tabla inflable + viento offshore
- Custom por spot

**Confianza**
- `alta` / `media` / `baja` según completitud de datos

#### Algoritmo de Riesgo

1. **Cálculo de dirección relativa del viento**
   - Onshore: viento hacia la playa (más seguro para deriva)
   - Offshore: viento hacia el mar (peligroso, te aleja)
   - Cross-shore: viento paralelo a la costa

2. **Evaluación de reglas base**
   - Viento > 30 km/h → `viento_fuerte`
   - Tabla inflable + viento offshore → `riesgo_deriva`
   - Olas > 1.5m → incrementa riesgo

3. **Evaluación de reglas específicas del spot**
   Ejemplo: "Si marea bajando + viento offshore en Varese → flag especial"

4. **Cálculo de scores**
   - Riesgo: suma ponderada de flags y condiciones
   - Esfuerzo: basado en viento vs potencia de remada
   - Disfrute: inverso a riesgo/esfuerzo, ajustado por experiencia

### Sistema Pedagógico (Layer B)

#### Proceso
1. Frontend envía resultado del motor + contexto a backend
2. Backend construye prompt para LLM con:
   - Perfil del usuario
   - Condiciones actuales
   - Scores y flags del motor
   - Glosario de términos (onshore, deriva, etc.)
3. LLM genera explicación educativa
4. Frontend muestra en sección "Sensei"

#### Características de Explicaciones
- **Tono**: Amigable, educativo, no alarmista
- **Estructura**: 
  - Por qué el score es así
  - Qué significa cada factor (viento, olas, marea)
  - Tips de seguridad específicos
- **Personalización**: Adaptada al nivel del usuario

---

## 🏗️ Arquitectura Técnica Propuesta

### Stack Recomendado (Mobile-First PWA)

**Frontend**
- **Framework**: Vite + React (o HTML/CSS/JS vanilla para máxima simplicidad)
- **PWA**: Service Workers para funcionalidad offline
- **Geolocalización**: Geolocation API del navegador
- **Diseño**: Mobile-first, solo funciona en pantallas táctiles
- **UI**: Estética oceánica moderna (ver especificaciones de diseño)

**Backend**
- **Opción 1 (Recomendada)**: Python FastAPI (ya existe, portarlo)
- **Opción 2**: Serverless/Edge Functions (Vercel/Netlify)
- **Opción 3**: Node.js + Express

**Datos Meteorológicos**
- API: OpenMeteo Marine API
- Endpoint: `https://marine-api.open-meteo.com/v1/marine`
- Parámetros: lat, lon, wave_height, wind_speed_10m, wind_direction_10m
- Frecuencia: Actualización cada 1 hora

**LLM**
- Google Gemini (`gemini-2.0-flash-exp`)
- Alternativa: OpenAI GPT-4

**Deploy**
- Frontend: Vercel / Netlify / GitHub Pages
- Backend: Railway / Render / Vercel Serverless

---

## 📱 UI/UX Specifications

### Detección de Dispositivo
- **Pantalla de entrada**: Si desktop, mostrar mensaje "Esta app solo funciona en móviles"
- **Geolocalización**: Solicitar permisos al cargar
- **Restricción geográfica**: Si ubicación > 50km de Mar del Plata, mostrar aviso

### Flujo de Usuario

#### 1. Landing / Onboarding (Primera vez)
Pantallas secuenciales:
1. **Bienvenida**
   - Logo + nombre "Rumbo SUP"
   - Tagline: "Tu instructor virtual de SUP"
   - Botón "Comenzar"

2. **Permisos**
   - Explicar por qué necesita ubicación
   - Botón "Activar ubicación"

3. **Perfil de Usuario**
   - Tipo de tabla (radio buttons con iconos)
   - Experiencia (slider visual)
   - Potencia de remada (selector 3 opciones)
   - Botón "Guardar y continuar"

#### 2. Pantalla Principal (Go/No-Go)

**Header**
- Spot detectado (e.g., "Varese")
- Hora de última actualización

**Indicador Principal** (Centro)
- Círculo grande con color:
  - Verde: riesgo bajo
  - Amarillo: riesgo medio
  - Rojo: riesgo alto
- Texto central: "GO" / "PRECAUCIÓN" / "NO-GO"

**Métricas (Cards)**
- Riesgo: Score + categoría + icono
- Esfuerzo: Score + categoría + icono
- Disfrute: Score + categoría + icono

**Condiciones Actuales** (Expandible)
- Viento: velocidad + dirección visual
- Olas: altura + icono
- Marea: estado (subiendo/bajando) + hora próxima

**Flags de Alerta** (Si existen)
- Lista de warnings (e.g., "⚠️ Viento fuerte")

**Botón "¿Por qué?" / "Modo Sensei"**
- CTA destacado para acceder a explicaciones

**Footer**
- Botón "Actualizar"
- Link a perfil de usuario

#### 3. Pantalla Sensei (Explicaciones)

**Header**
- Título: "Sensei te explica"
- Icono de sensei/maestro

**Contenido**
- Texto generado por IA en bloques legibles
- Formato markdown: negrita, listas, emojis

**Glosario** (Expandible)
- Tooltips o sección con términos técnicos

**Botón "Volver"**

#### 4. Pantalla de Perfil

- Ver/editar datos de usuario
- Botón "Guardar cambios"
- Link a "Acerca de" / "Cómo funciona"

### Design System

#### Paleta de Colores
```css
/* Primarios - Océano */
--ocean-deep: #0a1929;      /* Azul profundo */
--ocean-blue: #1976d2;       /* Azul medio */
--ocean-cyan: #00bcd4;       /* Cyan brillante */
--ocean-foam: #b2ebf2;       /* Espuma clara */

/* Semáforo de Riesgo */
--safe-green: #4caf50;       /* Verde seguro */
--caution-yellow: #ffc107;   /* Amarillo precaución */
--danger-red: #f44336;       /* Rojo peligro */

/* Neutrales */
--white: #ffffff;
--light-gray: #f5f5f5;
--dark-gray: #424242;
```

#### Tipografía
- **Principal**: Inter, Roboto, system-ui
- **Display**: Outfit para títulos

#### Animaciones
- Ondas sutiles en backgrounds
- Transitions suaves (0.3s ease)
- Micro-interacciones en botones
- Loading states con spinners oceánicos

#### Componentes Clave
- **Card**: Bordes redondeados, sombras suaves, padding generoso
- **Botones**: Primarios (solid), secundarios (outline), iconos
- **Indicador circular**: SVG animado con gradientes
- **Alerts/Flags**: Banners con iconos y colores contextuales

---

## 🔧 Especificaciones Técnicas

### API Backend - Endpoints Necesarios

#### `GET /api/health`
Health check simple
```json
Response: {"status": "ok"}
```

#### `POST /api/analyze`
Analiza condiciones para un spot y usuario

Request:
```json
{
  "spot_id": "varese",
  "user": {
    "board_type": "rigid",
    "experience": "intermediate",
    "paddle_power": "medium"
  }
}
```

Response:
```json
{
  "spot": {
    "name": "Varese",
    "lat": -37.9833,
    "lon": -57.5333
  },
  "weather": {
    "wind": {"speed_kmh": 25, "direction_deg": 135},
    "waves": {"height_m": 1.2},
    "tide": {"state": "rising"}
  },
  "result": {
    "scores": {"riesgo": 45, "esfuerzo": 60, "disfrute": 70},
    "categories": {"riesgo": "medio", "esfuerzo": "medio", "disfrute": "alto"},
    "flags": ["viento_moderado"],
    "confidence": "alta"
  }
}
```

#### `POST /api/pedagogy/explain`
Genera explicación educativa

Request:
```json
{
  "user": {...},
  "weather": {...},
  "result": {...}
}
```

Response:
```json
{
  "explanation": "**¿Por qué riesgo medio?**\n\nEl viento...",
  "glossary_terms": ["onshore", "deriva"]
}
```

#### `GET /api/spots/nearest?lat=X&lon=Y`
Retorna spot más cercano

Response:
```json
{
  "spot_id": "varese",
  "name": "Varese",
  "distance_km": 0.3
}
```

### Datos del Spot (Configuración)

```python
# Ejemplo: spots_config.py
SPOTS = {
    "varese": {
        "name": "Varese",
        "lat": -37.9833,
        "lon": -57.5333,
        "orientation_costa_deg": 90,  # Costa mira al Este
        "reglas_especificas": [
            {
                "condition": "tide_state == 'falling' and wind_dir_rel == 'offshore'",
                "flag": "deriva_varese",
                "descripcion": "Marea bajando + viento del oeste puede alejarte"
            }
        ]
    }
}
```

### OpenMeteo Integration

Request:
```python
params = {
    "latitude": -37.9833,
    "longitude": -57.5333,
    "hourly": "wave_height,wind_speed_10m,wind_direction_10m",
    "timezone": "America/Argentina/Buenos_Aires"
}
```

Procesar respuesta para obtener condición actual (hora más cercana).

### Persistencia de Usuario

**MVP**: LocalStorage del navegador
```javascript
localStorage.setItem('userProfile', JSON.stringify(profile));
```

**Futuro**: Backend con autenticación (JWT) + base de datos

---

## 📊 Plan de Desarrollo (Fases)

### Fase 1: MVP (1 semana)
- [ ] Landing con detección de móvil
- [ ] Onboarding de perfil
- [ ] Backend: endpoint `/analyze` con datos mock
- [ ] Pantalla Go/No-Go con indicador visual
- [ ] UI oceánica básica

### Fase 2: Datos Reales (1 semana)
- [ ] Integración OpenMeteo Marine API
- [ ] Geolocalización para detectar Varese
- [ ] Motor determinístico completo
- [ ] Testing en el terreno (Mar del Plata)

### Fase 3: IA Pedagógica (1 semana)
- [ ] Integración Gemini/GPT
- [ ] Pantalla Sensei funcional
- [ ] Prompt engineering para explicaciones
- [ ] Glosario de términos

### Fase 4: PWA & Refinamiento (1 semana)
- [ ] Service Workers para offline
- [ ] Iconos y manifest para instalación
- [ ] Optimización de performance
- [ ] Animaciones pulidas
- [ ] Testing exhaustivo

### Fase 5: Multi-Spot (Futuro)
- [ ] Agregar más spots de Mar del Plata
- [ ] Selector manual de spot
- [ ] Comparación de condiciones entre spots

---

## ✅ Criterios de Éxito

### Técnicos
- [ ] Funciona en Chrome/Safari móvil (iOS y Android)
- [ ] Geolocalización precisa (±100m)
- [ ] Respuesta del backend < 2s
- [ ] Funcionalidad offline básica (último resultado cached)
- [ ] Lighthouse score > 90 (performance, PWA)

### Funcionales
- [ ] Motor calcula riesgo coherente con condiciones reales
- [ ] Explicaciones de IA son educativas y relevantes
- [ ] UI intuitiva para usuarios sin experiencia técnica
- [ ] Flags de alerta se activan correctamente

### De Usuario
- [ ] Testeo con al menos 3 practicantes de SUP en MDQ
- [ ] Feedback positivo sobre utilidad y claridad
- [ ] Usuarios entienden el "por qué" de las recomendaciones

---

## 🚨 Restricciones y Consideraciones

### Técnicas
- Solo móviles (bloquear desktop)
- Requiere conexión para datos meteorológicos (offline solo caché)
- Precisión de OpenMeteo (datos cada 1 hora, interpolación)

### De Negocio
- MVP gratis, sin monetización inicial
- Escalabilidad futura a modelo SaaS (otras ciudades)
- Datos meteorológicos gratuitos (OpenMeteo tiene rate limits)

### Legales
- Disclaimer: "Esta app es educativa, no reemplaza juicio propio"
- No responsabilidad por decisiones de usuario
- Privacidad: datos de ubicación no se almacenan en backend

---

## 📝 Notas Importantes

### Filosofía "Split Brain"
Es **crítico** mantener la separación:
- Layer A (motor) debe ser 100% determinístico y auditable
- Layer B (IA) solo explica, nunca decide
- Si hay conflicto, Layer A prevalece siempre

### Seguridad
- El sistema debe ser **conservador** en riesgo
- Mejor prevenir (false positive) que permitir situación peligrosa
- Flags de alerta deben ser claros e imposibles de ignorar

### Educación sobre Lucro
- El valor principal es enseñar sobre condiciones oceánicas
- No es un "semáforo" simple, es un instructor
- Usuarios deben salir sabiendo MÁS sobre SUP

---

## 🎨 Referencias Visuales

### Inspiración de UI
- Windy.com (presentación de datos meteorológicos)
- Surfline (análisis de condiciones de surf)
- Material Design 3 (componentes modernos)

### Mood Board
- Paletas oceánicas profundas
- Micro-animaciones sutiles
- Glassmorphism en cards
- Gradientes de agua
- Iconografía limpia y moderna

---

## 🔗 Recursos Necesarios

### APIs
- OpenMeteo Marine: https://open-meteo.com/en/docs/marine-weather-api
- Google Gemini: https://ai.google.dev/

### Bibliotecas Frontend
- Geolocation API: nativa del navegador
- Chart.js o Recharts (para gráficos futuros)
- Framer Motion (animaciones)

### Herramientas
- Figma/Excalidraw para wireframes
- Lighthouse para auditoría PWA
- ngrok para testing móvil en desarrollo

---

## 💬 Preguntas para el Desarrollador

Antes de comenzar, considera:

1. **Stack backend**: ¿Prefieres FastAPI (Python) o algo más ligero como Vercel Serverless?
2. **Self-hosted vs Cloud**: ¿Dónde planeas deployar?
3. **LLM**: ¿Tienes API key de Gemini o prefieres otra opción?
4. **Testing**: ¿Tienes acceso a testers en Mar del Plata?
5. **Timeline**: ¿Cuánto tiempo puedes dedicar semanalmente?

---

## 📌 Próximos Pasos

1. Crear estructura de proyecto (mono-repo o separado frontend/backend)
2. Implementar pantalla de onboarding (frontend)
3. Desarrollar motor determinístico (backend)
4. Integrar OpenMeteo
5. Implementar UI oceánica
6. Conectar frontend-backend
7. Agregar Layer B (pedagógico)
8. Testing en Mar del Plata
9. Refinamiento basado en feedback

---

**¿Listo para comenzar? ¡Vamos a crear Rumbo SUP! 🏄**
