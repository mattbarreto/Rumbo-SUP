import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { triggerHaptic } from '../utils/haptics';
import './CircularIndicator.css';

function CircularIndicator({ seguridad, categoria, freshness = 'fresh' }) {
    // Alert haptic removed to prevent "Intervention" blocking on load.
    // Haptics should only occur on direct user interaction.

    // Map to design system semantic colors
    const getColorVariable = () => {
        if (categoria === 'alto') return 'var(--safety-safe)';
        if (categoria === 'medio') return 'var(--safety-warning)';
        return 'var(--safety-danger)';
    };

    const getText = () => {
        if (categoria === 'alto') return 'Condiciones seguras';
        if (categoria === 'medio') return 'Con precaución';
        return 'No recomendado';
    };

    const strokeColor = getColorVariable();
    const circumference = 2 * Math.PI * 85; // Inner ring radius
    const progress = (seguridad / 100) * circumference;

    // Animation logic
    // 'fresh' = slow calm breathing (4s)
    // 'alto' (Safe) = calm-glow vitality animation
    const isFresh = freshness === 'fresh';
    const isSafe = categoria === 'alto';

    return (
        <motion.div
            className={`circular-indicator ${isSafe ? 'calm-glow-animation' : ''}`}
            layoutId="safety-indicator"
        >
            <div className="breathing-ring-container">
                {/* Animated Glow Layer (Breathing) */}
                <motion.div
                    className="glow-layer"
                    style={{
                        background: `radial-gradient(circle, ${strokeColor.replace('var(', '').replace(')', '')} 0%, transparent 70%)`,
                        filter: 'blur(20px)',
                    }}
                    animate={{
                        opacity: isSafe ? [0.15, 0.4, 0.15] : (isFresh ? [0.1, 0.3, 0.1] : [0.1, 0.4, 0.1]),
                        scale: isSafe ? [1, 1.1, 1] : (isFresh ? [1, 1.05, 1] : [1, 1.08, 1]),
                    }}
                    transition={{
                        duration: isSafe ? 4 : (isFresh ? 4 : 1.5),
                        repeat: Infinity,
                        ease: 'easeInOut',
                    }}
                />

                {/* SVG with expanded viewBox to prevent clipping during breathing */}
                <svg
                    width="260"
                    height="260"
                    viewBox="-10 -10 220 220"
                    className="indicator-svg"
                    style={{ overflow: 'visible', color: strokeColor }}
                >
                    <defs>
                        {/* Glow filter for main ring */}
                        <filter id="glowFilter" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur stdDeviation="4" result="blur" />
                            <feComposite in="SourceGraphic" in2="blur" operator="over" />
                        </filter>

                        {/* Ripple Pattern for Stroke Texture */}
                        <pattern
                            id="ripple-pattern"
                            patternUnits="userSpaceOnUse"
                            width="10"
                            height="4"
                        >
                            <circle
                                cx="2"
                                cy="2"
                                r="1.5"
                                fill="currentColor"
                                opacity="0.8"
                            />
                            <circle
                                cx="6"
                                cy="2"
                                r="1.5"
                                fill="currentColor"
                                opacity="0.6"
                            />
                        </pattern>
                    </defs>

                    {/* Outer breathing ring */}
                    <motion.circle
                        cx="100"
                        cy="100"
                        r="95"
                        fill="none"
                        stroke={strokeColor}
                        strokeWidth="2"
                        opacity="0.3"
                        className="outer-ring"
                    />

                    {/* Track (Inner Background Circle) */}
                    <circle
                        cx="100"
                        cy="100"
                        r="85"
                        fill="var(--ocean-abyss)"
                        stroke="var(--glass-border)"
                        strokeWidth="1"
                    />

                    {/* Progress Arc - Main Ring with Safety Color */}
                    <motion.circle
                        cx="100"
                        cy="100"
                        r="85"
                        fill="none"
                        stroke="url(#ripple-pattern)"
                        strokeWidth="8"
                        strokeLinecap="round"
                        strokeDasharray={circumference}
                        strokeDashoffset={circumference - progress}
                        transform="rotate(-90 100 100)"
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset: circumference - progress }}
                        transition={{ duration: 1.5, ease: [0.22, 1, 0.36, 1] }}
                        style={{ filter: 'url(#glowFilter)' }}
                    />

                    {/* Shimmer highlight overlay on progress arc */}
                    <motion.circle
                        cx="100"
                        cy="100"
                        r="85"
                        fill="none"
                        stroke="url(#shimmerGradient)"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeDasharray={circumference}
                        strokeDashoffset={circumference - progress}
                        transform="rotate(-90 100 100)"
                        opacity="0.5"
                        animate={{
                            opacity: [0.3, 0.6, 0.3]
                        }}
                        transition={{
                            duration: 2,
                            repeat: Infinity,
                            ease: 'easeInOut'
                        }}
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

            {/* INDUSTRIAL STATUS BADGE - Layer A (Safety Cockpit) */}
            <motion.div
                className="indicator-label"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8, duration: 0.6 }}
            >
                <motion.div
                    className="status-badge status-badge--industrial"
                    style={{
                        backgroundColor: strokeColor,
                        color: 'var(--ocean-abyss)', // BLACK text on bright safety colors
                        fontWeight: 'var(--weight-bold)',
                        borderColor: strokeColor
                    }}
                    // Mechanical "lock-in" animation
                    initial={{ scale: 0.8, rotate: -5, opacity: 0 }}
                    animate={{ scale: 1, rotate: 0, opacity: 1 }}
                    transition={{
                        type: 'spring',
                        stiffness: 400,
                        damping: 15,
                        delay: 1
                    }}
                >
                    {getText()}
                </motion.div>
            </motion.div>
        </motion.div>
    );
}

export default CircularIndicator;
