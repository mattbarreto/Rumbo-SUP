// Conceptual Minimalist Icons for Rumbo SUP
// Phase 4 Refined: "Deep Ocean" Aesthetic
// Non-conventional, abstract, ultra-premium

export const AlertIcon = ({ className = "", size = 24, variant = "warning" }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        className={className}
    >
        {/* Alert Triangle: Minimalist warning */}
        <path
            d="M12 4L21 20H3L12 4Z"
            strokeWidth="1.5"
            strokeLinejoin="round"
            fill={variant === "danger" ? "currentColor" : "none"}
            opacity={variant === "danger" ? 0.2 : 1}
        />
        <line x1="12" y1="10" x2="12" y2="14" strokeWidth="2" strokeLinecap="round" />
        <circle cx="12" cy="17" r="1" fill="currentColor" stroke="none" />
    </svg>
);

export const WindIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        className={className}
        style={{ opacity: 0.9 }}
    >
        {/* Abstract Flow: Asymmetric tapering lines */}
        <path
            d="M2 12H18M2 8H14M2 16H22"
            strokeWidth="1.5"
            strokeLinecap="square"
        />
        {/* Motion dot */}
        <circle cx="20" cy="8" r="1.5" fill="currentColor" stroke="none" />
    </svg>
);

export const WaveIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        className={className}
    >
        {/* Harmonic Curve: Single perfect wave */}
        <path
            d="M2 15C5 15 7 10 12 10C17 10 19 15 22 15"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        />
        <path
            d="M2 19C5 19 7 15.5 10 15.5"
            strokeWidth="1.5"
            strokeLinecap="round"
            opacity="0.5"
        />
    </svg>
);

export const TideIcon = ({ className = "", size = 24, direction = "rising" }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        className={className}
    >
        {/* Vertical Gauge: Minimalist level indicator */}
        <line x1="12" y1="4" x2="12" y2="20" strokeWidth="1" opacity="0.4" />
        <circle
            cx="12"
            cy={direction === "rising" ? "8" : direction === "falling" ? "16" : "12"}
            r="4"
            fill="currentColor"
            stroke="none"
        />
        {/* Direction indicator */}
        {direction === "rising" && <path d="M18 10L12 4L6 10" strokeWidth="1.5" strokeLinecap="round" opacity="0.6" />}
        {direction === "falling" && <path d="M18 14L12 20L6 14" strokeWidth="1.5" strokeLinecap="round" opacity="0.6" />}
    </svg>
);

export const ShieldIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        className={className}
    >
        {/* Protective Orbit: Abstract safety */}
        <circle cx="12" cy="12" r="9" strokeWidth="1.5" opacity="0.3" />
        <path
            d="M12 3C12 3 12 8 12 12C12 16 16 21 16 21"
            strokeWidth="1.5"
            strokeLinecap="round"
        />
        <circle cx="12" cy="12" r="3" fill="currentColor" stroke="none" opacity="0.8" />
    </svg>
);

export const EffortIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        className={className}
    >
        {/* Pulse: Activity monitor abstract */}
        <path
            d="M3 12H6L9 6L15 18L18 12H21"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
        />
    </svg>
);

export const EnjoymentIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        className={className}
    >
        {/* Zenith: High point, sun abstract */}
        <circle cx="12" cy="12" r="4" fill="currentColor" stroke="none" />
        <path d="M12 4V6" strokeWidth="2" strokeLinecap="round" />
        <path d="M12 18V20" strokeWidth="2" strokeLinecap="round" />
        <path d="M4 12H6" strokeWidth="2" strokeLinecap="round" />
        <path d="M18 12H20" strokeWidth="2" strokeLinecap="round" />
        <path d="M6.34 6.34L7.75 7.75" strokeWidth="2" strokeLinecap="round" />
        <path d="M16.25 16.25L17.66 17.66" strokeWidth="2" strokeLinecap="round" />
        <path d="M6.34 17.66L7.75 16.25" strokeWidth="2" strokeLinecap="round" />
        <path d="M16.25 7.75L17.66 6.34" strokeWidth="2" strokeLinecap="round" />
    </svg>
);

export const LocationIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        className={className}
    >
        {/* Crosshair: Precision location */}
        <circle cx="12" cy="12" r="8" strokeWidth="1.5" />
        <line x1="12" y1="2" x2="12" y2="6" strokeWidth="1.5" />
        <line x1="12" y1="18" x2="12" y2="22" strokeWidth="1.5" />
        <line x1="2" y1="12" x2="6" y2="12" strokeWidth="1.5" />
        <line x1="18" y1="12" x2="22" y2="12" strokeWidth="1.5" />
        <circle cx="12" cy="12" r="2" fill="currentColor" stroke="none" />
    </svg>
);

export const RefreshIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        className={className}
    >
        {/* Open Loop: Minimalist refresh */}
        <path
            d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C15.5 3 18.5 5 20 8"
            strokeWidth="1.5"
            strokeLinecap="round"
        />
        <path d="M20 3V8H15" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
);

export const SettingsIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        className={className}
    >
        {/* Faders: Abstract control */}
        <line x1="6" y1="4" x2="6" y2="20" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />
        <line x1="12" y1="4" x2="12" y2="20" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />
        <line x1="18" y1="4" x2="18" y2="20" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />

        <circle cx="6" cy="14" r="2" fill="currentColor" stroke="none" />
        <circle cx="12" cy="8" r="2" fill="currentColor" stroke="none" />
        <circle cx="18" cy="16" r="2" fill="currentColor" stroke="none" />
    </svg>
);

export const BrainIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        className={className}
    >
        {/* Synapse: Network connection */}
        <circle cx="12" cy="12" r="3" fill="currentColor" stroke="none" />
        <circle cx="6" cy="8" r="1.5" strokeWidth="1.5" />
        <circle cx="18" cy="6" r="1.5" strokeWidth="1.5" />
        <circle cx="5" cy="17" r="1.5" strokeWidth="1.5" />
        <circle cx="19" cy="16" r="1.5" strokeWidth="1.5" />

        <path d="M12 12L6 8" strokeWidth="1" opacity="0.5" />
        <path d="M12 12L18 6" strokeWidth="1" opacity="0.5" />
        <path d="M12 12L5 17" strokeWidth="1" opacity="0.5" />
        <path d="M12 12L19 16" strokeWidth="1" opacity="0.5" />
    </svg>
);

export const TimeIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        className={className}
    >
        {/* Minimalist Hands: Just the hands, no face */}
        <path d="M12 6V12L16 14" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="12" cy="12" r="9" strokeWidth="1.5" opacity="0.4" />
    </svg>
);
