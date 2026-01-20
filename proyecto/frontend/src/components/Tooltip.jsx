import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './Tooltip.css';

/**
 * Tooltip Component - Contextual help for technical terms
 * Supports hover (desktop) and tap (mobile) interactions
 * Auto-positions to avoid viewport edges
 */
function Tooltip({ children, content, position = 'top' }) {
    const [isVisible, setIsVisible] = useState(false);
    const [calculatedPosition, setCalculatedPosition] = useState(position);
    const triggerRef = useRef(null);
    const tooltipRef = useRef(null);

    // Auto-adjust position to avoid viewport overflow
    useEffect(() => {
        if (isVisible && triggerRef.current && tooltipRef.current) {
            const triggerRect = triggerRef.current.getBoundingClientRect();
            const tooltipRect = tooltipRef.current.getBoundingClientRect();
            const viewportWidth = window.innerWidth;
            const viewportHeight = window.innerHeight;

            let newPosition = position;

            // Check if tooltip overflows right edge
            if (triggerRect.left + tooltipRect.width / 2 > viewportWidth - 20) {
                newPosition = 'left';
            }
            // Check if tooltip overflows left edge
            else if (triggerRect.left - tooltipRect.width / 2 < 20) {
                newPosition = 'right';
            }
            // Check if tooltip overflows top edge
            else if (triggerRect.top - tooltipRect.height < 20) {
                newPosition = 'bottom';
            }

            setCalculatedPosition(newPosition);
        }
    }, [isVisible, position]);

    const handleClick = (e) => {
        e.stopPropagation();
        setIsVisible(!isVisible);
    };

    const handleMouseEnter = () => setIsVisible(true);
    const handleMouseLeave = () => setIsVisible(false);

    // Close on outside click (mobile)
    useEffect(() => {
        const handleClickOutside = (e) => {
            if (triggerRef.current && !triggerRef.current.contains(e.target)) {
                setIsVisible(false);
            }
        };

        if (isVisible) {
            document.addEventListener('click', handleClickOutside);
            return () => document.removeEventListener('click', handleClickOutside);
        }
    }, [isVisible]);

    return (
        <span
            ref={triggerRef}
            className="tooltip-trigger"
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            onClick={handleClick}
            role="button"
            tabIndex={0}
            aria-label={`Más información sobre ${children}`}
            onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    setIsVisible(!isVisible);
                }
            }}
        >
            {children}

            <AnimatePresence>
                {isVisible && (
                    <motion.div
                        ref={tooltipRef}
                        className={`tooltip-content tooltip-${calculatedPosition}`}
                        initial={{ opacity: 0, scale: 0.9, y: calculatedPosition === 'top' ? 5 : -5 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9 }}
                        transition={{ duration: 0.15, ease: 'easeOut' }}
                        role="tooltip"
                    >
                        <div className="tooltip-arrow"></div>
                        {content}
                    </motion.div>
                )}
            </AnimatePresence>
        </span>
    );
}

export default Tooltip;
