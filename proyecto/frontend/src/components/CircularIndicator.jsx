import { motion } from 'framer-motion';
import './CircularIndicator.css';

function CircularIndicator({ seguridad, categoria }) {
    // Determinar color usando variables CSS del tema
    const getColorVariable = () => {
        if (categoria === 'alto') return 'var(--safe-teal)';
        if (categoria === 'medio') return 'var(--caution-amber)';
        return 'var(--danger-coral)';
    };

    const getStrokeColor = () => getColorVariable();

    // Determinar texto según categoría
    const getText = () => {
        if (categoria === 'alto') return 'Condiciones seguras';
        if (categoria === 'medio') return 'Con precaución';
        return 'No recomendado';
    };

    const strokeColor = getStrokeColor();
    // Getting raw hex for SVG defs might be tricky if we want exact matches to CSS vars without computing styles.
    // However, for SVG stroke we can use var() directly.

    const circumference = 2 * Math.PI * 90; // radio 90
    const progress = (seguridad / 100) * circumference;

    return (
        <div className="circular-indicator">
            <svg width="240" height="240" viewBox="0 0 200 200">
                <defs>
                    <linearGradient id="gradientSafety" x1="0%" y1="0%" x2="100%" y2="0%">
                        {/* We can't easily use var() inside stop-color in all browsers cleanly for gradients 
                             without knowing the underlying value, but we can try currentColor or use the specific hues.
                             For premium look, we'll try to stick to solid stroke with var() which is safer, 
                             or map manually to the HSL values if needed. 
                             Let's use the CSS variable directly in stroke, it works fine. 
                             Gradients for the stroke would require definitions.
                             Let's simple use a distinct opacity track.
                         */}
                    </linearGradient>
                    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="2" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                </defs>

                {/* Track (Background Circle) */}
                <circle
                    cx="100"
                    cy="100"
                    r="90"
                    fill="none"
                    stroke="var(--glass-border)"
                    strokeWidth="8"
                    opacity="0.5"
                />

                {/* Progress Circle with Animation */}
                <motion.circle
                    cx="100"
                    cy="100"
                    r="90"
                    fill="none"
                    stroke={strokeColor}
                    strokeWidth="8"
                    strokeLinecap="round"
                    strokeDasharray={circumference}
                    strokeDashoffset={circumference - progress}
                    transform="rotate(-90 100 100)"
                    initial={{ strokeDashoffset: circumference }}
                    animate={{ strokeDashoffset: circumference - progress }}
                    transition={{ duration: 1.5, ease: [0.22, 1, 0.36, 1] }}
                    style={{ filter: "url(#glow)" }}
                />

                {/* Central Score */}
                <text
                    x="100"
                    y="95"
                    textAnchor="middle"
                    fill="var(--text-primary)"
                    fontSize="56"
                    fontWeight="600"
                    fontFamily="var(--font-display)"
                    className="numeric"
                    dy="5"
                >
                    {Math.round(seguridad)}
                </text>

                <text
                    x="100"
                    y="125"
                    textAnchor="middle"
                    fill="var(--text-secondary)"
                    fontSize="12"
                    fontWeight="500"
                    fontFamily="var(--font-body)"
                    letterSpacing="0.1em"
                    style={{ textTransform: 'uppercase', opacity: 0.7 }}
                >
                    Seguridad
                </text>
            </svg>

            <motion.div
                className="indicator-label"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8, duration: 0.6 }}
            >
                <div
                    className="status-badge"
                    style={{
                        backgroundColor: `color-mix(in srgb, ${strokeColor} 20%, transparent)`,
                        color: strokeColor,
                        border: `1px solid color-mix(in srgb, ${strokeColor} 30%, transparent)`
                    }}
                >
                    {getText()}
                </div>
            </motion.div>
        </div>
    );
}

export default CircularIndicator;
