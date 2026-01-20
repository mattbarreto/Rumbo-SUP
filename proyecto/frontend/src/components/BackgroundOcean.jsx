import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import './BackgroundOcean.css';

function BackgroundOcean({ windSpeed = 10, safetyScore = 100, waveHeight = 0 }) {
    const causticsRef = useRef(null);

    // Calculate derived values for animation
    // Wind (0-60kmh) -> Intensity (0-1)
    const normalizedWind = Math.min((windSpeed || 0) / 40, 1);

    // Safety Color Logic
    let baseColor = 'var(--ocean-deep)';
    if (safetyScore !== null) {
        if (safetyScore <= 40) baseColor = 'var(--ocean-surface)'; // Turbid/Cyan
        else if (safetyScore <= 70) baseColor = 'var(--ocean-current)'; // Medium
        // > 70 keeps ocean-deep
    }

    useEffect(() => {
        // Parallax scroll effect for caustics (Preserved)
        const handleScroll = () => {
            if (causticsRef.current) {
                const scrollY = window.scrollY;
                causticsRef.current.style.transform = `translateY(${scrollY * 0.3}px)`;
            }
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    // Dynamic Gradient Style
    // We override the default gradient to inject the reactive baseColor
    const backgroundStyle = {
        background: `radial-gradient(circle at 50% 30%, ${baseColor} 0%, var(--ocean-abyss) 85%)`,
        transition: 'background 1s ease-in-out'
    };

    return (
        <div className="ocean-background" style={backgroundStyle}>
            <div className="ocean-noise"></div>
            <div className="ocean-caustics" ref={causticsRef}></div>

            {/* Reactive Ocean Wave Layer */}
            <motion.div
                className="ocean-reactive-wave"
                style={{
                    position: 'absolute',
                    bottom: 0,
                    left: 0,
                    width: '100%',
                    height: '30vh',
                    opacity: 0.1 + (normalizedWind * 0.1), // More wind = more visible wave
                    zIndex: -1
                }}
            >
                <motion.svg
                    viewBox="0 0 1440 320"
                    preserveAspectRatio="none"
                    style={{ width: '100%', height: '100%' }}
                    animate={{
                        y: [-10, -20 * (1 + normalizedWind), -10],
                        scaleY: [1, 1 + (normalizedWind * 0.1), 1]
                    }}
                    transition={{
                        duration: 6 / (0.5 + normalizedWind), // Faster with wind
                        repeat: Infinity,
                        ease: "easeInOut"
                    }}
                >
                    <path
                        fill="currentColor"
                        fillOpacity="1"
                        d="M0,192L48,197.3C96,203,192,213,288,229.3C384,245,480,267,576,250.7C672,235,768,181,864,181.3C960,181,1056,235,1152,234.7C1248,235,1344,181,1392,154.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
                        style={{ color: 'rgba(255,255,255,0.15)' }}
                    />
                </motion.svg>
            </motion.div>
        </div>
    );
}

export default BackgroundOcean;
