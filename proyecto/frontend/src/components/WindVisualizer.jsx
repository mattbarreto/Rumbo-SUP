import React from 'react';
import './WindVisualizer.css';

const WindVisualizer = ({ direction, speed, relativeDirection }) => {
    // direction: grados (0-360)
    // speed: km/h
    // relativeDirection: 'onshore' | 'offshore' | 'cross'

    // Determinar rotación de partículas segun relativeDirection
    // Asumimos costa abajo y mar arriba por defecto en el visual
    // Onshore: Mar (Arriba) -> Tierra (Abajo)
    // Offshore: Tierra (Abajo) -> Mar (Arriba)
    // Cross: Izquierda <-> Derecha

    // Simplificación visual:
    // Pintamos la costa como una linea curva en el bottom.
    // Mar es el area superior.

    let particleClass = "particle-flow-up"; // Offshore por defecto (Tierra -> Mar)

    if (relativeDirection === 'onshore') {
        particleClass = "particle-flow-down";
    } else if (relativeDirection === 'cross') {
        particleClass = "particle-flow-right";
    }

    // Velocidad de animación inversa (más rápido = menos duración)
    // 5 km/h -> 4s
    // 30 km/h -> 1s
    const baseDuration = Math.max(1, 4 - (speed / 10));

    // Cantidad de líneas basada en velocidad (min 8, max 24)
    const particleCount = Math.min(Math.max(Math.floor(speed / 1.5), 8), 24);

    // Generar partículas con propiedades orgánicas
    const particles = Array.from({ length: particleCount }).map((_, i) => ({
        id: i,
        // Distribución: Más densa cerca del horizonte (top 20-80% del contenedor)
        left: Math.random() * 100 + '%',
        top: Math.random() * 60 + 20 + '%',
        delay: Math.random() * -5 + 's', // Delay negativo para start instantáneo
        duration: (baseDuration * (0.8 + Math.random() * 0.4)) + 's', // Variación natural
        scale: 0.8 + Math.random() * 0.4, // Variación de tamaño
        opacity: 0.4 + Math.random() * 0.4 // Variación de visibilidad
    }));

    return (
        <div className="wind-visualizer glass-panel">
            <div className="wind-scene">
                {/* Partículas de viento - Streamlines Orgánicos */}
                <div className="particles-container">
                    {particles.map(p => (
                        <div
                            key={p.id}
                            className={`wind-particle-wrapper ${particleClass}`}
                            style={{
                                left: p.left,
                                top: p.top,
                                animationDuration: p.duration,
                                animationDelay: p.delay,
                                '--scale': p.scale,
                            }}
                        >
                            <svg
                                width="120"
                                height="20"
                                viewBox="0 0 120 20"
                                className="wind-streamline-svg"
                                preserveAspectRatio="none"
                            >
                                <defs>
                                    <linearGradient id="windGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                        <stop offset="0%" stopColor="white" stopOpacity="0" />
                                        <stop offset="50%" stopColor="white" stopOpacity="0.7" />
                                        <stop offset="100%" stopColor="white" stopOpacity="0" />
                                    </linearGradient>
                                </defs>
                                {/* Curva orgánica suave tipo "S" muy estirada */}
                                <path
                                    d="M0 10 C 40 14, 80 6, 120 10"
                                    fill="none"
                                    stroke="url(#windGradient)"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                />
                            </svg>
                        </div>
                    ))}
                </div>

                {/* Costa Estilizada */}
                <svg className="coastline-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
                    <path
                        d="M0,100 C30,90 70,90 100,100 L100,105 L0,105 Z"
                        fill="var(--ocean-sand)"
                        className="coast-land"
                    />
                    <text x="50" y="98" textAnchor="middle" className="coast-label">COSTA</text>
                </svg>

                {/* Info Text */}
                <div className="wind-info-overlay">
                    <span className="wind-speed">{Math.round(speed)} km/h</span>
                    <span className="wind-dir-label">
                        {relativeDirection === 'onshore' && "Onshore (Hacia costa)"}
                        {relativeDirection === 'offshore' && "Offshore (Hacia mar)"}
                        {relativeDirection === 'cross' && "Wind Cross (Paralelo)"}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default WindVisualizer;
