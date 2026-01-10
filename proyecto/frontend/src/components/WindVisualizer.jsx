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

    // Velocidad de animación basada en speed
    // speed alto -> duration bajo
    const animDuration = Math.max(0.5, 3 - (speed / 20)) + 's';

    // Generar partículas aleatorias
    const particles = Array.from({ length: 12 }).map((_, i) => ({
        id: i,
        left: Math.random() * 100 + '%',
        top: Math.random() * 100 + '%',
        delay: Math.random() * 2 + 's'
    }));

    return (
        <div className="wind-visualizer glass-panel">
            <div className="wind-scene">
                {/* Partículas de viento */}
                <div className="particles-container">
                    {particles.map(p => (
                        <div
                            key={p.id}
                            className={`wind-particle ${particleClass}`}
                            style={{
                                left: p.left,
                                top: p.top,
                                animationDuration: animDuration,
                                animationDelay: p.delay
                            }}
                        />
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
                    <text x="50" y="20" textAnchor="middle" className="sea-label">MAR</text>
                </svg>

                {/* Info Text */}
                <div className="wind-info-overlay">
                    <span className="wind-speed">{Math.round(speed)} km/h</span>
                    <span className="wind-dir-label">
                        {relativeDirection === 'onshore' && "Hacia la costa"}
                        {relativeDirection === 'offshore' && "Hacia el mar"}
                        {relativeDirection === 'cross' && "Paralelo"}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default WindVisualizer;
