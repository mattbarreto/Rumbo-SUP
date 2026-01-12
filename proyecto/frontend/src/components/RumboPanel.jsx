import React from 'react';
import { BrainIcon } from './Icons';
import './RumboPanel.css';

/**
 * RumboPanel - Layer B: Conversational AI Advice
 * Aesthetic: Chat Bubble / Organic vs Layer A's Industrial Cockpit
 * Typography: Instrument Sans (human, readable) vs Syne (display, industrial)
 */
function RumboPanel({ content, onClick }) {
    return (
        <div className="rumbo-panel" onClick={onClick} role="button" tabIndex={0}>
            <div className="rumbo-panel-header">
                <div className="rumbo-avatar">
                    <BrainIcon size={20} />
                </div>
                <span className="rumbo-label">Rumbo Dice:</span>
            </div>

            <p className="rumbo-content">
                {content}
            </p>

            {onClick && (
                <div className="rumbo-cta-hint">
                    <span>Más detalles</span>
                    <span>→</span>
                </div>
            )}
        </div>
    );
}

export default RumboPanel;
