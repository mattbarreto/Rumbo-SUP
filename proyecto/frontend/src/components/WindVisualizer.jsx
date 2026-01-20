import React from 'react';
import './WindVisualizer.css';

const WindVisualizer = ({ direction, speed, relativeDirection }) => {
    // direction: grados (0-360) (Compass: 0=N, 90=E, 180=S, 270=W)
    // relativeDirection: 'onshore' | 'offshore' | 'cross'

    // ==========================================
    // 1. WIND FLOW CALCULATION
    // ==========================================
    // Visual Base: CSS `flowHorizontal` moves Left -> Right (0deg visual).
    // Compass Mapping (Physics Driven):
    const windRotation = (direction + 90) % 360;

    // ==========================================
    // 2. COAST POSITIONING
    // ==========================================
    // Confiamos en relativeDirection del backend (ya usa rangos de MDP)
    // Si no viene, defaulteamos a 'cross' (no mostrar costa)
    const finalRelativeDirection = relativeDirection || 'cross';

    let coastRotation = 0;
    let showCoast = true;

    if (finalRelativeDirection === 'offshore') {
        coastRotation = windRotation + 180;
    } else if (finalRelativeDirection === 'onshore') {
        coastRotation = windRotation;
    } else {
        showCoast = false;
    }

    // ==========================================
    // 3. ANIMATION PHYSICS (MICRO-DUST / MIST)
    // ==========================================
    const canvasRef = React.useRef(null);
    const requestRef = React.useRef();
    const gustPhaseRef = React.useRef(0);
    const touchPosRef = React.useRef(null);

    React.useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const container = canvas.parentElement;

        const updateSize = () => {
            canvas.width = container.offsetWidth;
            canvas.height = container.offsetHeight;
        };
        updateSize();
        window.addEventListener('resize', updateSize);

        // Touch/Mouse interaction for Wind Wake
        const handleTouchStart = (e) => {
            const rect = canvas.getBoundingClientRect();
            const touch = e.touches ? e.touches[0] : e;
            touchPosRef.current = {
                x: touch.clientX - rect.left,
                y: touch.clientY - rect.top,
                active: true
            };
        };

        const handleTouchMove = (e) => {
            if (!touchPosRef.current) return;
            const rect = canvas.getBoundingClientRect();
            const touch = e.touches ? e.touches[0] : e;
            touchPosRef.current = {
                x: touch.clientX - rect.left,
                y: touch.clientY - rect.top,
                active: true
            };
        };

        const handleTouchEnd = () => {
            if (touchPosRef.current) {
                touchPosRef.current.active = false;
                setTimeout(() => { touchPosRef.current = null; }, 300);
            }
        };

        canvas.addEventListener('touchstart', handleTouchStart, { passive: true });
        canvas.addEventListener('touchmove', handleTouchMove, { passive: true });
        canvas.addEventListener('touchend', handleTouchEnd);
        canvas.addEventListener('mousedown', handleTouchStart);
        canvas.addEventListener('mousemove', handleTouchMove);
        canvas.addEventListener('mouseup', handleTouchEnd);
        canvas.addEventListener('mouseleave', handleTouchEnd);

        // ELITE PHYSICS CONFIGURATION
        // Depth Layers: Creates 3D parallax effect
        const layers = [
            { depth: 0.3, size: 0.6, opacity: 0.08, speed: 0.7, color: 'rgba(224, 242, 254, 0.3)' },  // Far (background)
            { depth: 0.6, size: 1.0, opacity: 0.20, speed: 1.0, color: 'rgba(224, 242, 254, 0.6)' },  // Mid
            { depth: 1.0, size: 1.6, opacity: 0.35, speed: 1.3, color: 'rgba(224, 242, 254, 0.9)' },  // Near (foreground)
        ];

        const particleCount = 280; // Reduced for better performance with layers
        const particles = [];

        // Create particles with layer assignment
        for (let i = 0; i < particleCount; i++) {
            const layerIndex = Math.floor(Math.random() * 3);
            const layer = layers[layerIndex];

            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                layerIndex,
                size: (Math.random() * 0.6 + 0.7) * layer.size, // Size varies within layer
                speedMultiplier: Math.random() * 0.4 + 0.6,
                baseOpacity: (Math.random() * 0.2 + 0.8) * layer.opacity,
                opacity: 0,
                // Lifecycle for fade in/out
                age: 0,
                lifetime: Math.random() * 400 + 300, // 300-700 frames
                // Multi-frequency turbulence
                wigglePhase1: Math.random() * Math.PI * 2,
                wigglePhase2: Math.random() * Math.PI * 2,
                wigglePhase3: Math.random() * Math.PI * 2,
                wiggleSpeed1: Math.random() * 0.015 + 0.01,
                wiggleSpeed2: Math.random() * 0.035 + 0.023,
                wiggleSpeed3: Math.random() * 0.008 + 0.007,
                // Pulse
                pulseOffset: Math.random() * Math.PI * 2,
                pulseSpeed: Math.random() * 0.04 + 0.015,
            });
        }

        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Wind Gusts: Periodic intensity waves
            gustPhaseRef.current += 0.0008; // Slow evolution
            const gustStrength = Math.sin(gustPhaseRef.current) * 0.5 + 0.5; // 0-1
            const gustBoost = 1 + (gustStrength * 0.35); // +0% to +35%

            // Physics Vector
            const rad = (windRotation * Math.PI) / 180;
            const flowSpeed = Math.min(Math.max(speed * 0.12, 0.5), 3.5);

            const dx = Math.cos(rad) * flowSpeed;
            const dy = Math.sin(rad) * flowSpeed;

            // Perpendicular vector for turbulence
            const perpX = -Math.sin(rad);
            const perpY = Math.cos(rad);

            particles.forEach((p, i) => {
                const layer = layers[p.layerIndex];

                // 1. Multi-Frequency Turbulence (Organic movement)
                p.wigglePhase1 += p.wiggleSpeed1;
                p.wigglePhase2 += p.wiggleSpeed2;
                p.wigglePhase3 += p.wiggleSpeed3;

                const turbulence =
                    Math.sin(p.wigglePhase1) * 0.3 +      // Base frequency
                    Math.sin(p.wigglePhase2) * 0.15 +     // High frequency (detail)
                    Math.sin(p.wigglePhase3) * 0.5;       // Low frequency (drift)

                // 2. Movement with Gust + Layer parallax
                let moveX = dx * p.speedMultiplier * layer.speed * gustBoost;
                let moveY = dy * p.speedMultiplier * layer.speed * gustBoost;

                // Apply turbulence perpendicular to flow
                moveX += perpX * turbulence;
                moveY += perpY * turbulence;

                // 3. ELITE: Clustering (Emergent grouping)
                // Check only nearby particles for performance
                let clusterForceX = 0;
                let clusterForceY = 0;
                const checkRange = Math.min(10, particles.length - i - 1);

                for (let j = i + 1; j < i + 1 + checkRange && j < particles.length; j++) {
                    const p2 = particles[j];
                    const dist = Math.hypot(p2.x - p.x, p2.y - p.y);

                    // Attract within range 10-50px
                    if (dist > 10 && dist < 50) {
                        const angle = Math.atan2(p2.y - p.y, p2.x - p.x);
                        const strength = (50 - dist) / 50 * 0.04; // Very subtle
                        clusterForceX += Math.cos(angle) * strength;
                        clusterForceY += Math.sin(angle) * strength;
                    }
                }

                moveX += clusterForceX;
                moveY += clusterForceY;

                // 4. ELITE: Wind Wake (Touch interaction)
                if (touchPosRef.current && touchPosRef.current.active) {
                    const touchRadius = 45;
                    const dist = Math.hypot(p.x - touchPosRef.current.x, p.y - touchPosRef.current.y);

                    if (dist < touchRadius) {
                        const repelAngle = Math.atan2(p.y - touchPosRef.current.y, p.x - touchPosRef.current.x);
                        const repelStrength = (touchRadius - dist) / touchRadius;
                        moveX += Math.cos(repelAngle) * repelStrength * 4;
                        moveY += Math.sin(repelAngle) * repelStrength * 4;
                    }
                }

                p.x += moveX;
                p.y += moveY;

                // 5. Lifecycle Fade (Cinematographic spawn/despawn)
                p.age++;
                const lifecycle = p.age / p.lifetime;

                let fadeMultiplier = 1;
                if (lifecycle < 0.12) {
                    // Fade in
                    fadeMultiplier = lifecycle / 0.12;
                } else if (lifecycle > 0.92) {
                    // Fade out
                    fadeMultiplier = (1 - lifecycle) / 0.08;
                }

                // 6. Pulse (Glimmer effect)
                p.pulseOffset += p.pulseSpeed;
                const pulse = Math.sin(p.pulseOffset) * 0.12;

                p.opacity = Math.max(0, Math.min(1,
                    (p.baseOpacity + pulse) * fadeMultiplier
                ));

                // 7. Respawn when lifecycle ends
                if (p.age >= p.lifetime) {
                    p.age = 0;
                    // Respawn at edge based on flow direction
                    if (Math.abs(dx) > Math.abs(dy)) {
                        p.x = dx > 0 ? -10 : canvas.width + 10;
                        p.y = Math.random() * canvas.height;
                    } else {
                        p.x = Math.random() * canvas.width;
                        p.y = dy > 0 ? -10 : canvas.height + 10;
                    }
                }

                // 8. Wrap around (backup for edge cases)
                const buffer = 15;
                if (p.x > canvas.width + buffer) p.x = -buffer;
                if (p.x < -buffer) p.x = canvas.width + buffer;
                if (p.y > canvas.height + buffer) p.y = -buffer;
                if (p.y < -buffer) p.y = canvas.height + buffer;

                // 9. Draw with layer-specific color
                ctx.fillStyle = layer.color;
                ctx.globalAlpha = p.opacity;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();
            });

            requestRef.current = requestAnimationFrame(animate);
        };

        requestRef.current = requestAnimationFrame(animate);

        return () => {
            window.removeEventListener('resize', updateSize);
            canvas.removeEventListener('touchstart', handleTouchStart);
            canvas.removeEventListener('touchmove', handleTouchMove);
            canvas.removeEventListener('touchend', handleTouchEnd);
            canvas.removeEventListener('mousedown', handleTouchStart);
            canvas.removeEventListener('mousemove', handleTouchMove);
            canvas.removeEventListener('mouseup', handleTouchEnd);
            canvas.removeEventListener('mouseleave', handleTouchEnd);
            cancelAnimationFrame(requestRef.current);
        };
    }, [windRotation, speed]);

    return (
        <div className="wind-visualizer glass-panel">
            <div className="wind-scene">

                {/* LAYER 1: COAST (Context) */}
                {showCoast && (
                    <div
                        className="coast-container"
                        style={{
                            position: 'absolute',
                            width: '100%',
                            height: '100%',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            transform: `rotate(${coastRotation}deg)`,
                            pointerEvents: 'none',
                            zIndex: 1
                        }}
                    >
                        <svg
                            viewBox="0 0 100 100"
                            preserveAspectRatio="none"
                            style={{
                                position: 'absolute',
                                right: '-20%',
                                top: '-50%',
                                width: '60%',
                                height: '200%',
                                overflow: 'visible'
                            }}
                        >
                            <path
                                d="M80,0 Q60,50 80,100 L100,100 L100,0 Z"
                                fill="var(--ocean-sand)"
                                className="coast-land"
                            />
                            <text
                                x="90"
                                y="50"
                                textAnchor="middle"
                                fill="rgba(0,0,0,0.4)"
                                style={{ fontSize: '6px', fontWeight: 'bold', textTransform: 'uppercase', writingMode: 'vertical-rl' }}
                            >
                                Costa
                            </text>
                        </svg>
                    </div>
                )}

                {/* LAYER 2: CANVAS PARTICLES (Micro-Dust) */}
                <canvas
                    ref={canvasRef}
                    className="particles-canvas"
                    style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        zIndex: 5,
                        pointerEvents: 'none'
                    }}
                />

                {/* LAYER 3: INFO OVERLAY */}
                <div className="wind-info-overlay" style={{ zIndex: 20 }}>
                    <span className="wind-speed">{Math.round(speed)} km/h</span>
                    <span className="wind-dir-label">
                        {finalRelativeDirection === 'onshore' && "Onshore"}
                        {finalRelativeDirection === 'offshore' && "Offshore"}
                        {finalRelativeDirection === 'cross' && "Cross"}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default WindVisualizer;
