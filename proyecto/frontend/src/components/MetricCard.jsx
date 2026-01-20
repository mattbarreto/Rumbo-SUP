import { motion } from 'framer-motion';
import './MetricCard.css';

/**
 * INDUSTRIAL METRIC CARD - Safety Cockpit Component
 * 
 * Features:
 * - Dynamic styling based on data values (safe=green, danger=red pulse)
 * - High contrast for outdoor sunlight legibility
 * - Tabular numbers for consistent data scanning
 * - NO overlapping (clarity over aesthetics)
 */
import { useSpring, animated } from 'react-spring';

function MetricCard({ label, value, unit, icon, threshold }) {
    // Determine severity based on threshold
    const getSeverity = () => {
        if (!threshold) return 'neutral';
        if (value === null || value === undefined) return 'neutral';

        if (label.toLowerCase().includes('viento') || label.toLowerCase().includes('wind')) {
            // Wind thresholds (km/h)
            if (value <= 10) return 'safe';
            if (value <= 20) return 'warning';
            return 'danger';
        }

        if (label.toLowerCase().includes('ola') || label.toLowerCase().includes('wave')) {
            // Wave height thresholds (m)
            if (value <= 0.5) return 'safe';
            if (value <= 1.2) return 'warning';
            return 'danger';
        }

        // Generic score-based (0-100)
        if (value >= 70) return 'safe';
        if (value >= 40) return 'warning';
        return 'danger';
    };

    const severity = getSeverity();

    // Get safety color
    const getSafetyColor = () => {
        switch (severity) {
            case 'safe': return 'var(--safety-safe)';
            case 'warning': return 'var(--safety-warning)';
            case 'danger': return 'var(--safety-danger)';
            default: return 'var(--ocean-shimmer)';
        }
    };

    const safetyColor = getSafetyColor();

    // Spring Animation for Value
    // Distinguish between numeric values (animate) and non-numeric values (display as-is)
    const parsedValue = Number(value);
    const isValidNumber = !isNaN(parsedValue) && isFinite(parsedValue) && value !== null && value !== undefined;
    const numericValue = isValidNumber ? parsedValue : 0;

    // Only animate if we have a valid number
    const { val } = useSpring({
        from: { val: 0 },
        val: numericValue,
        config: { mass: 1, tension: 40, friction: 20 }
    });

    return (
        <motion.div
            className={`metric-card metric-card--${severity}`}
            data-severity={severity}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
        >
            {/* Industrial border indicator */}
            <div
                className="metric-card__indicator"
                style={{ backgroundColor: safetyColor }}
            />

            <div className="metric-card__header">
                {icon && <span className="metric-card__icon">{icon}</span>}
                <span className="metric-card__label">{label}</span>
            </div>

            <div className="metric-card__body">
                <animated.div className="metric-card__value">
                    {value === null || value === undefined
                        ? '-'
                        : isValidNumber
                            ? val.to(v => {
                                // Smart formatting: if original value implies decimals (e.g. wave), keep 1 decimal
                                // otherwise round
                                if (label.toLowerCase().includes('ola') || label.toLowerCase().includes('wave')) {
                                    return v.toFixed(1);
                                }
                                return Math.round(v);
                            })
                            : value /* Display non-numeric values as-is (e.g. "45°") */
                    }
                </animated.div>
                <span className="metric-card__unit">{value !== null && value !== undefined ? unit : ''}</span>
            </div>

            {/* Danger pulse glow */}
            {severity === 'danger' && (
                <motion.div
                    className="metric-card__danger-glow"
                    style={{ backgroundColor: safetyColor }}
                    animate={{
                        opacity: [0.2, 0.4, 0.2],
                        scale: [0.95, 1, 0.95]
                    }}
                    transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: 'easeInOut'
                    }}
                />
            )}
        </motion.div>
    );
}

export default MetricCard;
