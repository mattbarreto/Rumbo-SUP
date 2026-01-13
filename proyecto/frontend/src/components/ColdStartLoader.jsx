import React from 'react';
import './ColdStartLoader.css';

/**
 * ColdStartLoader - Loading indicator for Render.com cold starts
 * Pure CSS animations, 0KB JS overhead
 * Shows when backend takes >3s to respond (cold start scenario)
 */
function ColdStartLoader() {
    return (
        <div className="cold-start-overlay">
            <div className="cold-start-container">
                {/* Animated waves background */}
                <div className="wave-loader">
                    <div className="wave wave-1"></div>
                    <div className="wave wave-2"></div>
                    <div className="wave wave-3"></div>
                </div>

                {/* Central breathing circle */}
                <div className="loader-circle">
                    <svg viewBox="0 0 100 100" className="circle-svg">
                        <circle
                            cx="50"
                            cy="50"
                            r="45"
                            className="breathing-ring"
                        />
                    </svg>
                </div>

                {/* Loading text */}
                <div className="loader-content">
                    <h2 className="loader-title">Despertando el servidor...</h2>
                    <p className="loader-subtitle">
                        Render.com está activando la API
                        <span className="dot-1">.</span>
                        <span className="dot-2">.</span>
                        <span className="dot-3">.</span>
                    </p>
                    <p className="loader-info">
                        Primera carga puede tardar ~30 segundos
                    </p>
                </div>
            </div>
        </div>
    );
}

export default ColdStartLoader;
