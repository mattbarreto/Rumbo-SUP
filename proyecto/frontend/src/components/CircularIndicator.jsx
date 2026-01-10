import { motion } from 'framer-motion';
import './CircularIndicator.css';

function CircularIndicator({ seguridad, categoria }) {
    // Map to design system semantic colors
    const getColorVariable = () => {
        if (categoria === 'alto') return 'var(--ocean-kelp)';
        if (categoria === 'medio') return 'var(--ocean-coral)';
        return 'var(--ocean-urchin)';
    };

    const getText = () => {
        if (categoria === 'alto') return 'Condiciones seguras';
        if (categoria === 'medio') return 'Con precaución';
        return 'No recomendado';
    };

    const strokeColor = getColorVariable();
    const circumference = 2 * Math.PI * 85; // Inner ring radius
    const progress = (seguridad / 100) * circumference;

    return (
        <div className="circular-indicator">
            <div className="breathing-ring-container">
                {/* Animated Glow Layer (Breathing) */}
                <motion.div
                    className="glow-layer"
                    style={{
                        background: `radial-gradient(circle, ${strokeColor.replace('var(', '').replace(')', '')} 0%, transparent 70%)`,
                        filter: 'blur(20px)',
                    }}
                    animate={{
                        opacity: [0.2, 0.4, 0.2],
                        scale: [1, 1.05, 1],
                    }}
                    transition={{
                        duration: 4,
                        repeat: Infinity,
                        ease: 'easeInOut',
                    }}
                />

                <svg width="240" height="240" viewBox="0 0 200 200" className="indicator-svg">
                    <defs>
                        <filter id="glowFilter" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur stdDeviation="3" result="blur" />
                            <feComposite in="SourceGraphic" in2="blur" operator="over" />
                        </filter>
                    </defs>

                    {/* Outer Ring (50% opacity, 2px) */}
                    <circle
                        cx="100"
                        cy="100"
                        r="95"
                        fill="none"
                        stroke={strokeColor}
                        strokeWidth="2"
                        opacity="0.5"
                        className="outer-ring"
                    />

                    {/* Track (Inner Background Circle) */}
                    <circle
                        cx="100"
                        cy="100"
                        r="85"
                        fill="var(--ocean-abyss)"
                        stroke="var(--glass-border)"
                        strokeWidth="3"
                    />

                    {/* Progress Arc (Inner Ring) */}
                    <motion.circle
                        cx="100"
                        cy="100"
                        r="85"
                        fill="none"
                        stroke={strokeColor}
                        strokeWidth="6"
                        strokeLinecap="round"
                        strokeDasharray={circumference}
                        strokeDashoffset={circumference - progress}
                        transform="rotate(-90 100 100)"
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset: circumference - progress }}
                        transition={{ duration: 1.5, ease: [0.22, 1, 0.36, 1] }}
                        style={{ filter: 'url(#glowFilter)' }}
                    />

                    {/* Central Score (Display size) */}
                    <text
                        x="100"
                        y="95"
                        textAnchor="middle"
                        fill="var(--ocean-sand)"
                        fontSize="56"
                        fontWeight="600"
                        fontFamily="var(--font-display)"
                        letterSpacing="-0.5px"
                        dy="5"
                    >
                        {Math.round(seguridad)}
                    </text>

                    {/* Label */}
                    <text
                        x="100"
                        y="128"
                        textAnchor="middle"
                        fill="var(--ocean-driftwood)"
                        fontSize="11"
                        fontWeight="500"
                        fontFamily="var(--font-body)"
                        letterSpacing="2px"
                    >
                        SEGURIDAD
                    </text>
                </svg>
            </div>

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
