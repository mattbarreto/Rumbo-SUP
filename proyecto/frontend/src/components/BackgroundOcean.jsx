import React, { useEffect, useRef } from 'react';
import './BackgroundOcean.css';

function BackgroundOcean() {
    const causticsRef = useRef(null);

    useEffect(() => {
        // Parallax scroll effect for caustics
        const handleScroll = () => {
            if (causticsRef.current) {
                const scrollY = window.scrollY;
                // Move caustics at 0.3x scroll speed for parallax effect
                causticsRef.current.style.transform = `translateY(${scrollY * 0.3}px)`;
            }
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <div className="ocean-background">
            <div className="ocean-noise"></div>
            <div className="ocean-caustics" ref={causticsRef}></div>
            {/* Optional: Add bubbles or other atmospheric elements here */}
        </div>
    );
}

export default BackgroundOcean;
