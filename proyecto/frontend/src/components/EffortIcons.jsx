import React from 'react';

/**
 * RUMBO SUP - Effort Icons (Paddle Stroke)
 * 
 * Design Language: Oceanic Minimalism
 * Anatomy: Real SUP paddle shape
 *   - T-Grip handle (ergonomic top grip)
 *   - Long thin shaft
 *   - Teardrop/elongated blade (characteristic of SUP paddles)
 * 
 * Semantic Orientation:
 *   - Handle UP (in the air, held by paddler)
 *   - Blade DOWN (submerged in water)
 *   - Water layer overlaps blade for depth illusion
 * 
 * Colors: ocean-shimmer (#61A5C2), ocean-foam (#A9D6E5), coral accents
 */

// Colores del design system - Usando variables CSS para permitir override dinámico
const COLORS = {
    paddle: 'var(--icon-paddle, #F5F1EB)',        // ocean-sand
    paddleShade: 'var(--icon-paddle-shade, #E8E4DC)', // ocean-shell
    waterCalm: 'var(--icon-water, #61A5C2)',     // ocean-shimmer
    waterFoam: 'var(--icon-foam, #A9D6E5)',     // ocean-foam
    splash: 'var(--icon-splash, #EF4444)',        // Default legacy red
    splashLight: 'var(--icon-splash-light, #FCA5A5)',
};

export const EffortLowIcon = ({ size = 28, className = '' }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 48 48"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={className}
    >
        {/* SUP Paddle - Vertical, calm position */}
        <g>
            {/* T-Grip Handle (characteristic of SUP paddles) */}
            <rect x="19" y="2" width="10" height="4" rx="2" fill={COLORS.paddle} />
            <rect x="22" y="5" width="4" height="3" fill={COLORS.paddle} />

            {/* Shaft (long and thin) */}
            <rect x="22.5" y="8" width="3" height="22" fill={COLORS.paddle} />

            {/* Blade (teardrop shape - wider at bottom) */}
            <path
                d="M24 30 L20 32 L18 40 L19 44 L24 46 L29 44 L30 40 L28 32 Z"
                fill={COLORS.paddle}
            />
            <path
                d="M24 32 L21 34 L20 40 L24 43 L28 40 L27 34 Z"
                fill={COLORS.paddleShade}
                opacity="0.3"
            />
        </g>

        {/* Water surface (calm ripples) - Overlaps blade */}
        <ellipse cx="24" cy="38" rx="18" ry="3" fill="#0D1B2A" opacity="0.4" />
        <path
            d="M4 38 Q12 36 20 38 Q28 40 36 38 Q42 36 46 38"
            stroke={COLORS.waterCalm}
            strokeWidth="1.5"
            fill="none"
            opacity="0.8"
        />
        <path
            d="M8 42 Q16 40 24 42 Q32 44 40 42"
            stroke={COLORS.waterFoam}
            strokeWidth="1"
            fill="none"
            opacity="0.5"
        />
    </svg>
);

export const EffortMediumIcon = ({ size = 28, className = '' }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 48 48"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={className}
    >
        {/* SUP Paddle - Angled stroke (action position) */}
        <g transform="rotate(-20 24 24)">
            {/* T-Grip Handle */}
            <rect x="18" y="0" width="10" height="4" rx="2" fill={COLORS.paddle} />
            <rect x="21" y="3" width="4" height="3" fill={COLORS.paddle} />

            {/* Shaft */}
            <rect x="21.5" y="6" width="3" height="20" fill={COLORS.paddle} />

            {/* Blade (teardrop) */}
            <path
                d="M23 26 L19 28 L17 36 L18 40 L23 42 L28 40 L29 36 L27 28 Z"
                fill={COLORS.paddle}
            />
            <path
                d="M23 28 L20 30 L19 36 L23 39 L27 36 L26 30 Z"
                fill={COLORS.paddleShade}
                opacity="0.3"
            />
        </g>

        {/* Wave motion (active water) */}
        <path
            d="M2 36 Q10 30 18 36 Q26 42 34 36 Q42 30 48 34"
            stroke={COLORS.waterCalm}
            strokeWidth="2"
            fill="none"
            opacity="0.9"
        />
        <path
            d="M0 42 Q10 38 20 42 Q30 46 40 42 Q46 40 48 42"
            stroke={COLORS.waterFoam}
            strokeWidth="1.5"
            fill="none"
            opacity="0.6"
        />
    </svg>
);

export const EffortHighIcon = ({ size = 28, className = '' }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 48 48"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={className}
    >
        {/* SUP Paddle - Strong angle (power stroke) */}
        <g transform="rotate(-30 24 28)">
            {/* T-Grip Handle */}
            <rect x="17" y="-2" width="10" height="4" rx="2" fill={COLORS.paddle} />
            <rect x="20" y="1" width="4" height="3" fill={COLORS.paddle} />

            {/* Shaft */}
            <rect x="20.5" y="4" width="3" height="20" fill={COLORS.paddle} />

            {/* Blade (deeper in water) */}
            <path
                d="M22 24 L18 26 L16 34 L17 38 L22 40 L27 38 L28 34 L26 26 Z"
                fill={COLORS.paddle}
            />
        </g>

        {/* Splash droplets */}
        <circle cx="8" cy="22" r="2.5" fill={COLORS.splash} opacity="0.85" />
        <circle cx="42" cy="18" r="3" fill={COLORS.splash} opacity="0.9" />
        <circle cx="12" cy="14" r="1.5" fill={COLORS.splashLight} opacity="0.7" />
        <circle cx="38" cy="26" r="2" fill={COLORS.splash} opacity="0.75" />
        <circle cx="5" cy="32" r="1.5" fill={COLORS.splashLight} opacity="0.6" />
        <circle cx="44" cy="30" r="1.5" fill={COLORS.splashLight} opacity="0.6" />

        {/* Choppy waves */}
        <path
            d="M0 38 Q8 30 16 38 Q24 46 32 38 Q40 30 48 36"
            stroke={COLORS.splash}
            strokeWidth="2.5"
            fill="none"
            opacity="0.9"
        />
        <path
            d="M4 44 Q12 40 20 44 Q28 48 36 44 Q44 40 48 44"
            stroke={COLORS.splash}
            strokeWidth="1.5"
            fill="none"
            opacity="0.5"
        />
    </svg>
);

export default { EffortLowIcon, EffortMediumIcon, EffortHighIcon };
