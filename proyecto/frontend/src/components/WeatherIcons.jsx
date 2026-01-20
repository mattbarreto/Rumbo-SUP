import React from 'react';

/**
 * RUMBO SUP - Weather & UI Icons
 * Style: Oceanic Minimalism (Inline SVG)
 */

const COLORS = {
    primary: '#A9D6E5',   // ocean-foam
    secondary: '#61A5C2', // ocean-shimmer
    accent: '#FF7043',    // coral
    text: '#F5F1EB'       // ocean-sand
};

export const WindIconMinimal = ({ size = 24, className = '' }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" className={className} xmlns="http://www.w3.org/2000/svg">
        <path d="M4 12H20" stroke={COLORS.primary} strokeWidth="2" strokeLinecap="round" />
        <path d="M6 8H18C19.1046 8 20 7.10457 20 6C20 4.89543 19.1046 4 18 4" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" />
        <path d="M8 16H16C17.1046 16 18 16.8954 18 18C18 19.1046 17.1046 20 16 20" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" />
    </svg>
);

export const DirectionIconMinimal = ({ size = 24, className = '' }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" className={className} xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="10" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M12 6L14 11L12 18L10 11L12 6Z" fill={COLORS.primary} />
    </svg>
);

export const WaveIconMinimal = ({ size = 24, className = '' }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" className={className} xmlns="http://www.w3.org/2000/svg">
        <path d="M2 13.6C2 13.6 5 10 9 10C13 10 14 14 18 14C22 14 22 10 22 10" stroke={COLORS.primary} strokeWidth="2" strokeLinecap="round" />
        <path d="M4 18C4 18 6 16 9 16C12 16 13 18 16 18C19 18 20 16 20 16" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" />
    </svg>
);

export const UpdateIconMinimal = ({ size = 24, className = '' }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" className={className} xmlns="http://www.w3.org/2000/svg">
        <path d="M21 12C21 16.9706 16.9706 21 12 21C9.69494 21 7.59227 20.1332 6 18.7083L3 16" stroke={COLORS.primary} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M3 12C3 7.02944 7.02944 3 12 3C14.3051 3 16.4077 3.86683 18 5.29168L21 8" stroke={COLORS.primary} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M21 3V8H16" stroke={COLORS.primary} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M3 21V16H8" stroke={COLORS.primary} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
);

export const BrainIconMinimal = ({ size = 24, className = '' }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" className={className} xmlns="http://www.w3.org/2000/svg">
        <path d="M9.5 8C8.5 8 8 9 8 9" stroke={COLORS.accent} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M15.5 8C16.5 8 17 9 17 9" stroke={COLORS.accent} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <rect x="5" y="11" width="14" height="8" rx="4" stroke={COLORS.primary} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="12" cy="15" r="2" fill={COLORS.secondary} />
        <path d="M12 5V8" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M12 3L14 5H10L12 3Z" fill={COLORS.primary} opacity="0.8" />
    </svg>
);

export const ShieldIconMinimal = ({ size = 24, className = '' }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" className={className} xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="9" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" opacity="0.5" />
        <path d="M12 3C12 3 12 8 12 12C12 16 16 21 16 21" stroke={COLORS.primary} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="12" cy="12" r="3" fill={COLORS.primary} stroke="none" opacity="0.9" />
    </svg>
);

export const EffortIconMinimal = ({ size = 24, className = '' }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" className={className} xmlns="http://www.w3.org/2000/svg">
        <path d="M3 12H6L9 6L15 18L18 12H21" stroke={COLORS.primary} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
);

export const EnjoymentIconMinimal = ({ size = 24, className = '' }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" className={className} xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="4" fill={COLORS.primary} stroke="none" />
        <path d="M12 4V6" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" />
        <path d="M12 18V20" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" />
        <path d="M4 12H6" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" />
        <path d="M18 12H20" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" />
        <path d="M6.34 6.34L7.75 7.75" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" />
        <path d="M16.25 16.25L17.66 17.66" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" />
        <path d="M6.34 17.66L7.75 16.25" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" />
        <path d="M16.25 7.75L17.66 6.34" stroke={COLORS.secondary} strokeWidth="2" strokeLinecap="round" />
    </svg>
);

// Exports grouped
export default {
    WindIconMinimal,
    DirectionIconMinimal,
    WaveIconMinimal,
    UpdateIconMinimal,
    BrainIconMinimal,
    ShieldIconMinimal,
    EffortIconMinimal,
    EnjoymentIconMinimal
};
