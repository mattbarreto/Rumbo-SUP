# Guía de Contribución

Gracias por tu interés en contribuir a Rumbo SUP.

## Código de Conducta

Este proyecto sigue un código de conducta simple: ser respetuoso, colaborativo y constructivo.

---

## Reportar Bugs

1. Verifica que el bug no haya sido reportado en [Issues](https://github.com/mattbarreto/rumbo-sup/issues)
2. Crea un nuevo issue con:
   - Título claro (ej. "WindVisualizer no muestra partículas en iOS Safari")
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Screenshots si aplica
   - Entorno (navegador, versión, dispositivo)

## Sugerir Features

1. Abre un issue con el tag `enhancement`
2. Describe el problema que resuelve, la solución propuesta y alternativas consideradas

---

## Pull Requests

### Preparación

```bash
# Fork el proyecto
git clone https://github.com/TU_USUARIO/rumbo-sup.git

# Crea un branch desde main
git checkout -b feature/nombre-descriptivo

# Configura upstream
git remote add upstream https://github.com/mattbarreto/rumbo-sup.git
```

### Desarrollo

1. Sigue las guías de estilo (ver abajo)
2. Escribe tests si aplica
3. Documenta funciones complejas

### Commits

Usa [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: agregar filtro de spots por región
fix: corregir cálculo de viento offshore
docs: actualizar README con nueva API
style: aplicar border-radius a AboutScreen
refactor: optimizar clustering en WindVisualizer
```

### Enviar

```bash
git push origin feature/nombre-descriptivo
```

Crea el Pull Request en GitHub con descripción de cambios e issue relacionada.

---

## Guías de Estilo

### JavaScript/React

```javascript
// Nombres descriptivos, no abreviaciones
const WindVisualizer = ({ direction, speed }) => {
  const [particles, setParticles] = useState([]);
  
  // Comentarios para lógica compleja
  const flowSpeed = Math.min(Math.max(speed * 0.12, 0.5), 3.5);
  
  return <div className="wind-visualizer">{/* ... */}</div>;
};
```

- Componentes en PascalCase
- Variables en camelCase
- Max 100 caracteres por línea

### Python

```python
def calculate_seguridad(weather: WeatherData, flags: List[str]) -> float:
    """
    Calcula score de seguridad (0-100).
    
    Args:
        weather: Datos meteorológicos actuales
        flags: Lista de alertas detectadas
        
    Returns:
        Score donde 100 = máxima seguridad
    """
    score = 100.0
    if "riesgo_deriva" in flags:
        score -= 60
    return max(0.0, score)
```

- Type hints obligatorios
- Docstrings estilo Google
- Black formatter (line-length=100)

### CSS

```css
.wind-visualizer {
  width: 100%;
  border-radius: var(--radius-lg);
  background: var(--ocean-deep);
}
```

- Usar variables CSS siempre que sea posible
- Mobile-first (min-width media queries)

---

## Testing

```bash
# Frontend
npm test

# Backend
pytest
```

---

## Estructura de Branches

```
main        # Producción
feature/*   # Nuevas features
fix/*       # Bug fixes
docs/*      # Documentación
```

---

## Proceso de Review

1. Lint pass
2. Tests pass
3. Build succeeds
4. Code review aprobado
5. Merge a main (squash si hay muchos commits)

---

## Contacto

¿Dudas? Abre un issue con el tag `question`.
