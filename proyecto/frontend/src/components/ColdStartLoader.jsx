import React from 'react';
import './ColdStartLoader.css';

/**
 * ColdStartLoader - Calm, clear loading indicator for Render.com cold starts
 * Design: Two concentric rings + clear text hierarchy
 * Feeling: System waking up, not failing
 */
function ColdStartLoader() {
    return (
        <div className="cold-start-overlay">
            <div className="cold-start-container">
                {/* Two concentric rings - geometric center shared */}
                <div className="rings-container">
                    <svg viewBox="0 0 200 200" className="rings-svg">
                        {/* Outer ring - thinner, lower opacity, slower */}
                        <circle
                            cx="100"
                            cy="100"
                            r="80"
                            className="ring ring-outer"
                        />
                        {/* Inner ring - slightly thicker, medium opacity, gentle */}
                        <circle
                            cx="100"
                            cy="100"
                            r="60"
                            className="ring ring-inner"
                        />
                    </svg>
                </div>

                {/* Text block - separated, clear hierarchy */}
                <div className="text-container">
                    <p className="text-primary">Despertando el servidor…</p>
                    <p className="text-secondary">Activando la Guía de Mar</p>
                </div>
            </div>
        </div>
    );
}

export default ColdStartLoader;
