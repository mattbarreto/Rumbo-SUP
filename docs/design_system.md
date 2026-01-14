# SUP Sensei Design System

## 1. Design Philosophy
**"Oceanic Minimalist"**
- **Core Feeling:** Calm, rhythmic, deep, and organic.
- **Metaphor:** The interface mimics the ocean—from the deep "Abyss" background to the "Surface" accents and "Spray" glass effects.
- **Motion:** Animations should "breathe" (4s cycle) or "flow" like waves (6s cycle), never abrupt.

---

## 2. Design Tokens

### 2.1 Color Palette
The colors are derived from deep ocean tones, moving from dark backgrounds to light accents.

#### Primary Tones (The Water)
| Token | Hex | Usage |
|-------|-----|-------|
| `ocean.abyss` | `#0A1628` | **Main Background**. The deepest depth. |
| `ocean.deep` | `#0F2942` | Surface elements, card backgrounds (gradient start). |
| `ocean.current`| `#1A4667` | Elevated surfaces, card backgrounds (gradient end). |
| `ocean.surface`| `#2A6F97` | Secondary accents, active states. |
| `ocean.shimmer`| `#61A5C2` | **Primary Brand Color**. Highlights, icons, active text. |
| `ocean.foam` | `#A9D6E5` | Subtle text details, secondary icons. |

#### Neutrals (The Shore)
| Token | Hex | Usage |
|-------|-----|-------|
| `ocean.sand` | `#F5F1EB` | **Primary Text**. Warm white, readable against deep blue. |
| `ocean.shell` | `#E8E4DC` | Secondary text, placeholders. |
| `ocean.driftwood`| `#C4BFB5` | Muted text, labels, borders. |

#### Semantic Status (Life Indicators)
| Token | Hex | Meaning |
|-------|-----|---------|
| `ocean.kelp` | `#52796F` | **Safe / Go**. Healthy state. |
| `ocean.coral` | `#E07A5F` | **Caution / Attention**. |
| `ocean.urchin` | `#9B2335` | **Danger / Stop**. High risk. |

#### Transparency & Glass
- **Mist**: `rgba(169, 214, 229, 0.1)` (Overlay)
- **Spray**: `rgba(97, 165, 194, 0.15)` (Glass containers, buttons)

---

### 2.2 Typography
Uses system sans-serif fonts (San Francisco/Roboto) to maintain cleanliness.
**Scale Ratio**: ~1.618 (Golden Ratio).

| Size Token | Value (px) | Usage |
|------------|------------|-------|
| `xs` | 11 | Metadata, small tags |
| `sm` | 13 | Labels, secondary details |
| `base` | 16 | Body text, buttons |
| `lg` | 20 | Subheaders |
| `xl` | 26 | Card numerical values |
| `2xl` | 34 | Section Headers |
| `3xl` | 42 | Impact text |
| `display` | 56 | Large score indicators |

**Tracking (Letter Spacing):**
- **Tight (-0.5)**: Large headers (`2xl`+).
- **Wide (1.0)**: Uppercase labels, small text.
- **Widest (2.0)**: Very small uppercase tags (e.g., "RIESGO").

---

### 2.3 Spacing & Layout
**Grid Base**: 8pt.

- `xs`: 4px
- `sm`: 8px
- `md`: 16px (Standard padding)
- `lg`: 24px (Section gap)
- `xl`: 32px
- `2xl`: 48px

### 2.4 Shadows & Glows
Shadows are used to create "underwater diffusion" rather than hard elevation.
- **Soft**: `ocean.shimmer` at 15% opacity, Y+4, blur 12.
- **Glow**: `ocean.shimmer` at 30% opacity, centered, blur 20.

---

## 3. UI Components

### 3.1 Ocean Card
The primary container for information.
- **Background**: Linear Gradient from `ocean.deep` (Top-Left) to `ocean.current` (Bottom-Right).
- **Border**: 1px solid `ocean.current` (or subtle transparency).
- **Radius**: `16px` (radius.lg).
- **Content**: Padding `16px`.

### 3.2 Glass Card (Premium)
Used for special overlays or premium features.
- **Background**: `rgba(15, 23, 42, 0.6)` + Bloom/Blur effect.
- **Border**: Gradient border (Top-Left Light to Bottom-Right Transparent).
- **Effect**: `BlurView` (intensity ~10-20).

### 3.3 Breathing Ring (Indicator)
The central visual element for "Go/No-Go" status.
- **Structure**:
  1. **Inner Circle**: Solid `ocean.abyss` background, 2-3px colored border.
  2. **Outer Ring**: 2px border, 50% opacity, slightly larger.
  3. **Glow Layer**: Absolute position, large blur radius.
- **Animation**:
  - The Glow Layer pulses opacity (0.2 -> 0.4) and scale (1.0 -> 1.05) in a 3-4s loop (`timing.breath`).

### 3.4 Buttons
- **Standard Button**: Background `ocean.spray` (glassy blue), Radius `radius.lg` (24px).
- **Premium Button**: Horizontal Linear Gradient (e.g., Sky Blue to Deep Blue), Shadow `ocean.shimmer`.

---

## 4. Motion & Atmospherics

### 4.1 Wave Background
The app should never feel static.
- **Implementation**:
  - Base Layer: Vertical Gradient (`ocean.abyss` -> `ocean.deep`).
  - Wave Layer 1: Low opacity (`0.3`), slow loop (6s).
  - Wave Layer 2: Lower opacity (`0.15`), slower loop (8s), offset phase.
- **Feel**: Like looking at deep water calmly moving.

### 4.2 Timings
- `wave`: 6000ms (Backgrounds)
- `breath`: 4000ms (Indicators, rings)
- `transition`: 300ms (Page fades, slides)
