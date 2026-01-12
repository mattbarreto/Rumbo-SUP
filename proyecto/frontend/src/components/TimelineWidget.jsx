import React from 'react';
import './TimelineWidget.css';

const TimelineWidget = ({ timeline, onPointSelect, selectedIndex }) => {
    // Si no hay timeline, no renderizar nada o skeleton
    if (!timeline || timeline.length === 0) return null;

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

                            {/* Optional: We can keep the effort icon or remove it to reduce noise. 
                                Keeping it small for now as per "Thumb Zone" usually implies less clutter, 
                                but user didn't explicitly ask to remove it. */}
                            <span className="effort-mini-icon" title={`Esfuerzo: ${effort}`}>
                                {effort === 'alto' && '🔥'}
                                {effort === 'medio' && '💧'}
                                {effort === 'bajo' && '😌'}
                            </span>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default TimelineWidget;
