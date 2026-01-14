import React from 'react';
import './TimelineWidget.css';
import { EffortLowIcon, EffortMediumIcon, EffortHighIcon } from './EffortIcons';

const TimelineWidget = ({ timeline, onPointSelect, selectedIndex }) => {
    // Si no hay timeline, no renderizar nada o skeleton
    if (!timeline || timeline.length === 0) return null;

    // Mapeo de nivel de esfuerzo a componente SVG
    const getEffortIcon = (effort) => {
        switch (effort) {
            case 'bajo':
                return <EffortLowIcon size={28} className="effort-icon" />;
            case 'medio':
                return <EffortMediumIcon size={28} className="effort-icon" />;
            case 'alto':
                return <EffortHighIcon size={28} className="effort-icon" />;
            default:
                return <EffortMediumIcon size={28} className="effort-icon" />;
        }
    };

    return (
        <div className="timeline-widget">
            <h3 className="section-title">Timeline del Día</h3>
            <div className="timeline-scroll-container">
                {timeline.map((point, index) => {
                    const score = point.result.scores.seguridad;
                    const effort = point.result.categories.esfuerzo;

                    // Traffic Light Logic
                    let statusClass = "status-danger"; // < 50
                    if (score >= 80) statusClass = "status-safe";
                    else if (score >= 50) statusClass = "status-caution";

                    const isSelected = selectedIndex === index;

                    return (
                        <div
                            key={index}
                            className={`timeline-block ${statusClass} ${isSelected ? 'selected' : ''}`}
                            onClick={() => onPointSelect(point, index)}
                        >
                            <span className="time-label">{point.hour_label}</span>

                            {/* Traffic Light Indicator */}
                            <div className="traffic-light-indicator"></div>

                            {/* Effort Icon (SVG - Transparent) */}
                            <div className="effort-icon-wrapper" title={`Esfuerzo: ${effort}`}>
                                {getEffortIcon(effort)}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default TimelineWidget;


