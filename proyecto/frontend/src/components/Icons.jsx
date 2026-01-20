// Conceptual Minimalist Icons for Rumbo SUP
// Phase 4 Refined: "Deep Ocean" Aesthetic (Updated)
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
        {/* Organic Warning: Soft rounded triangle, buoy-like */}
        <path
            d="M10.29 3.86L1.82 18C1.645 18.302 1.553 18.645 1.553 18.995C1.553 19.345 1.645 19.688 1.82 19.99C1.995 20.292 2.247 20.544 2.549 20.719C2.851 20.894 3.194 20.986 3.544 20.986H20.456C20.806 20.986 21.149 20.894 21.451 20.719C21.753 20.544 22.005 20.292 22.18 19.99C22.355 19.688 22.447 19.345 22.447 18.995C22.447 18.645 22.355 18.302 22.18 18L13.71 3.86C13.535 3.558 13.283 3.306 12.981 3.131C12.679 2.956 12.336 2.864 11.986 2.864C11.636 2.864 11.293 2.956 10.991 3.131C10.689 3.306 10.437 3.558 10.262 3.86"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            fill={variant === "danger" ? "currentColor" : "none"}
            opacity={variant === "danger" ? 0.2 : 1}
        />
        <path d="M12 2C12 2 12 16 12 16" strokeWidth="2" strokeLinecap="round" />
        {/* Simplified clean path for better rendering */}
        <path d="M12 8V15" strokeWidth="2.5" strokeLinecap="round" />
        <circle cx="12" cy="18.5" r="1.5" fill="currentColor" stroke="none" />
    </svg>
);

export const WindIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
    >
        {/* Abstract Flow: Asymmetric tapering lines with wave element */}
        <path d="M2 12H18" />
        <path d="M2 8H14" />
        <path d="M2 16H22" />
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
            strokeWidth="2"
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
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
    >
        {/* Vertical Gauge: Minimalist level indicator */}
        <line x1="12" y1="4" x2="12" y2="20" opacity="0.4" />
        <circle
            cx="12"
            cy={direction === "rising" ? "8" : direction === "falling" ? "16" : "12"}
            r="4"
            fill="currentColor"
            stroke="none"
        />
        {/* Direction indicator */}
        {direction === "rising" && <path d="M18 10L12 4L6 10" opacity="0.6" />}
        {direction === "falling" && <path d="M18 14L12 20L6 14" opacity="0.6" />}
    </svg>
);

export const ShieldIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
    >
        {/* Protective Orbit: Abstract safety */}
        <circle cx="12" cy="12" r="9" opacity="0.3" />
        <path d="M12 3C12 3 12 8 12 12C12 16 16 21 16 21" />
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
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
    >
        {/* Pulse: Activity monitor abstract */}
        <path d="M3 12H6L9 6L15 18L18 12H21" />
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
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
    >
        {/* Crosshair: Precision location */}
        <circle cx="12" cy="12" r="8" />
        <line x1="12" y1="2" x2="12" y2="6" />
        <line x1="12" y1="18" x2="12" y2="22" />
        <line x1="2" y1="12" x2="6" y2="12" />
        <line x1="18" y1="12" x2="22" y2="12" />
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
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
    >
        {/* Open Loop: Minimalist refresh */}
        <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C15.5 3 18.5 5 20 8" />
        <path d="M20 3V8H15" />
    </svg>
);

export const SettingsIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
    >
        {/* Faders: Abstract control */}
        <line x1="6" y1="4" x2="6" y2="20" opacity="0.3" />
        <line x1="12" y1="4" x2="12" y2="20" opacity="0.3" />
        <line x1="18" y1="4" x2="18" y2="20" opacity="0.3" />

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
        {/* Organic Brain: Fluid waves forming mind structure */}
        <path
            d="M9.5 20C9.5 20 5 19.5 3 15C1 10.5 4 6 8 5C8 5 9 2 14 3C19 4 21 8 21 12C21 16 18 20 14.5 20"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        />
        <path
            d="M10 11.5C10 11.5 11 15 14 14"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            opacity="0.6"
        />
        <path
            d="M14 8C14 8 16 9 16 11"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            opacity="0.6"
        />
    </svg>
);

export const TimeIcon = ({ className = "", size = 24 }) => (
    <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
    >
        {/* Minimalist Hands: Just the hands, no face */}
        <path d="M12 6V12L16 14" />
        <circle cx="12" cy="12" r="9" opacity="0.4" />
    </svg>
);

export const GithubIcon = ({ className = "", size = 24 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <path d="M12 2C6.47 2 2 6.47 2 12C2 16.42 5.31 20.17 9.5 21.17C10 21.26 10.19 20.96 10.19 20.72C10.19 20.5 10.18 19.91 10.18 19.13C7.23 19.78 6.4 17.96 6.16 17.29C6.03 16.94 5.43 15.86 4.9 15.58C4.46 15.34 3.84 14.88 4.89 14.86C5.87 14.85 6.57 15.76 6.8 16.13C7.94 18.06 9.77 17.5 10.49 17.17C10.6 16.35 10.93 15.8 11.3 15.48C8.56 15.17 5.68 14.11 5.68 9.38C5.68 8.03 6.16 6.94 6.96 6.07C6.83 5.76 6.41 4.5 7.08 2.81C7.08 2.81 8.11 2.48 10.45 4.07C11.43 3.8 12.48 3.66 13.53 3.66C14.58 3.66 15.63 3.8 16.61 4.07C18.95 2.48 19.98 2.81 19.98 2.81C20.66 4.5 20.24 5.76 20.11 6.07C20.91 6.94 21.39 8.03 21.39 9.38C21.39 14.12 18.51 15.16 15.76 15.47C16.23 15.87 16.65 16.67 16.65 17.89C16.65 19.64 16.64 21.06 16.64 21.28C16.64 21.52 16.82 21.83 17.33 21.73C21.51 20.17 24 16.32 24 12C24 6.47 18.53 2 12 2Z" />
    </svg>
);

export const LinkedinIcon = ({ className = "", size = 24 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <path d="M16 8C17.5913 8 19.1174 8.63214 20.2426 9.75736C21.3679 10.8826 22 12.4087 22 14V21H18V14C18 13.4696 17.7893 12.9609 17.4142 12.5858C17.0391 12.2107 16.5304 12 16 12C15.4696 12 14.9609 12.2107 14.5858 12.5858C14.2107 12.9609 14 13.4696 14 14V21H10V14C10 12.4087 10.6321 10.8826 11.7574 9.75736C12.8826 8.63214 14.4087 8 16 8Z" />
        <path d="M6 9H2V21H6V9Z" />
        <path d="M4 6C5.10457 6 6 5.10457 6 4C6 2.89543 5.10457 2 4 2C2.89543 2 2 2.89543 2 4C2 5.10457 2.89543 6 4 6Z" />
    </svg>
);

export const GlobeIcon = ({ className = "", size = 24 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <circle cx="12" cy="12" r="10" />
        <path d="M2.05 12.5H22" opacity="0.5" />
        <path d="M12 2A15.3 15.3 0 0 1 17.05 12A15.3 15.3 0 0 1 12 22A15.3 15.3 0 0 1 6.95 12A15.3 15.3 0 0 1 12 2Z" opacity="0.8" />
    </svg>
);

export const CodeIcon = ({ className = "", size = 24 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <path d="M16 18L22 12L16 6" />
        <path d="M8 6L2 12L8 18" />
    </svg>
);

export const ShareIcon = ({ className = "", size = 24 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <circle cx="18" cy="5" r="3" />
        <circle cx="6" cy="12" r="3" />
        <circle cx="18" cy="19" r="3" />
        <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" />
        <line x1="15.41" y1="6.51" x2="8.59" y2="10.49" />
    </svg>
);


export const InfoIcon = ({ className = "", size = 24 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <circle cx="12" cy="12" r="10" opacity="0.8" />
        {/* Liquid Info: Drop shape and soft line */}
        <path d="M12 16V12" />
        <path d="M12 8.5C12.5523 8.5 13 8.05228 13 7.5C13 6.94772 12.5523 6.5 12 6.5C11.4477 6.5 11 6.94772 11 7.5C11 8.05228 11.4477 8.5 12 8.5Z" fill="currentColor" />
    </svg>
);

export const ArrowLeftIcon = ({ className = "", size = 24 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        {/* Fluid Arrow: Curved shaft like a current */}
        <path d="M20 12H4" />
        <path d="M10 18L4 12L10 6" />
    </svg>
);

export const SeeIcon = ({ className = "", size = 24 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        {/* Ocean Horizon: Scanning the sea - curved observation line */}
        <path d="M2 12C4 9 8 6 12 6C16 6 20 9 22 12" />
        <path d="M2 12C4 15 8 18 12 18C16 18 20 15 22 12" opacity="0.4" />
        {/* Focus point: wave crest */}
        <circle cx="12" cy="12" r="2" opacity="0.8" />
    </svg>
);

export const BodyIcon = ({ className = "", size = 24 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        {/* Balance Wave: Body as flowing water finding equilibrium */}
        <path d="M12 3C12 3 12 8 12 12C12 16 12 21 12 21" opacity="0.3" />
        <path d="M6 12C6 12 9 9 12 9C15 9 18 12 18 12C18 12 15 15 12 15C9 15 6 12 6 12Z" />
        {/* Floating center of gravity */}
        <circle cx="12" cy="12" r="2" fill="currentColor" opacity="0.6" />
    </svg>
);

export const IdeaIcon = ({ className = "", size = 24 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
        {/* Navigation Star: Strategy as celestial guidance over ocean */}
        <path d="M12 2L14 8L20 9L15 14L17 20L12 17L7 20L9 14L4 9L10 8L12 2Z" opacity="0.8" />
        {/* Radiating clarity */}
        <circle cx="12" cy="11" r="3" opacity="0.4" />
    </svg>
);

export const TargetIcon = ({ className = "", size = 24 }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" className={className}>
        {/* Compass Rose: Focus as finding true north */}
        <circle cx="12" cy="12" r="8" strokeWidth="2" opacity="0.4" />
        <path d="M12 4L12 8M12 16L12 20M4 12L8 12M16 12L20 12" strokeWidth="2" strokeLinecap="round" />
        <circle cx="12" cy="12" r="3" strokeWidth="2" />
        <circle cx="12" cy="12" r="1" fill="currentColor" />
    </svg>
);

