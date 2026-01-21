import { useState, useRef, useEffect, useLayoutEffect } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import './Tooltip.css';

/**
 * Tooltip Component - Contextual help for technical terms
 * Uses Portal + Fixed positioning to escape parent overflow constraints
 */
function Tooltip({ children, content, position = 'top' }) {
    const [isVisible, setIsVisible] = useState(false);
    const [coords, setCoords] = useState({ top: 0, left: 0, arrowLeft: '50%' });
    const [finalPosition, setFinalPosition] = useState(position);
    const triggerRef = useRef(null);
    const tooltipRef = useRef(null);

    // Calculate position using layout effect (before paint)
    useLayoutEffect(() => {
        if (isVisible && triggerRef.current) {
            const triggerRect = triggerRef.current.getBoundingClientRect();
            const viewportWidth = window.innerWidth;
            const viewportHeight = window.innerHeight;
            const margin = 12;
            const tooltipEstimatedWidth = 220; // max-width from CSS
            const tooltipEstimatedHeight = 80; // estimated height

            let newPosition = position;
            let top = 0;
            let left = 0;

            // Vertical position calculation
            if (position === 'top') {
                top = triggerRect.top - tooltipEstimatedHeight - 8;
                if (top < margin) {
                    newPosition = 'bottom';
                    top = triggerRect.bottom + 8;
                }
            } else {
                top = triggerRect.bottom + 8;
                if (top + tooltipEstimatedHeight > viewportHeight - margin) {
                    newPosition = 'top';
                    top = triggerRect.top - tooltipEstimatedHeight - 8;
                }
            }

            // Horizontal position - center on trigger
            const triggerCenterX = triggerRect.left + triggerRect.width / 2;
            left = triggerCenterX - tooltipEstimatedWidth / 2;

            // Clamp to viewport with arrow adjustment
            let arrowOffset = 0;
            if (left < margin) {
                arrowOffset = left - margin;
                left = margin;
            } else if (left + tooltipEstimatedWidth > viewportWidth - margin) {
                arrowOffset = (left + tooltipEstimatedWidth) - (viewportWidth - margin);
                left = viewportWidth - margin - tooltipEstimatedWidth;
            }

            // Arrow position (percentage from center + offset)
            const arrowLeft = `calc(50% + ${arrowOffset}px)`;

            setFinalPosition(newPosition);
            setCoords({ top, left, arrowLeft });
        }
    }, [isVisible, position]);

    // Refine position after tooltip actually renders (for accurate dimensions)
    useEffect(() => {
        if (isVisible && tooltipRef.current && triggerRef.current) {
            const triggerRect = triggerRef.current.getBoundingClientRect();
            const tooltipRect = tooltipRef.current.getBoundingClientRect();
            const viewportWidth = window.innerWidth;
            const margin = 12;

            // Recalculate with actual tooltip width
            const triggerCenterX = triggerRect.left + triggerRect.width / 2;
            let left = triggerCenterX - tooltipRect.width / 2;

            let arrowOffset = 0;
            if (left < margin) {
                arrowOffset = left - margin;
                left = margin;
            } else if (left + tooltipRect.width > viewportWidth - margin) {
                arrowOffset = (left + tooltipRect.width) - (viewportWidth - margin);
                left = viewportWidth - margin - tooltipRect.width;
            }

            const arrowLeft = `calc(50% + ${arrowOffset}px)`;

            // Update top based on actual height
            let top = coords.top;
            if (finalPosition === 'top') {
                top = triggerRect.top - tooltipRect.height - 8;
            } else {
                top = triggerRect.bottom + 8;
            }

            setCoords(prev => ({ ...prev, top, left, arrowLeft }));
        }
    }, [isVisible, finalPosition]);

    const handleClick = (e) => {
        e.stopPropagation();
        setIsVisible(!isVisible);
    };

    const handleMouseEnter = () => setIsVisible(true);
    const handleMouseLeave = () => setIsVisible(false);

    // Close on outside click or scroll
    useEffect(() => {
        const handleClickOutside = (e) => {
            if (triggerRef.current && !triggerRef.current.contains(e.target)) {
                setIsVisible(false);
            }
        };
        const handleScroll = () => setIsVisible(false);

        if (isVisible) {
            document.addEventListener('click', handleClickOutside);
            document.addEventListener('scroll', handleScroll, true);
            return () => {
                document.removeEventListener('click', handleClickOutside);
                document.removeEventListener('scroll', handleScroll, true);
            };
        }
    }, [isVisible]);

    // Portal renders tooltip at body level - escapes all overflow:hidden
    const tooltipElement = (
        <AnimatePresence>
            {isVisible && (
                <motion.div
                    ref={tooltipRef}
                    className={`tooltip-content tooltip-fixed tooltip-${finalPosition}`}
                    style={{
                        position: 'fixed',
                        top: coords.top,
                        left: coords.left,
                        zIndex: 9999
                    }}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    transition={{ duration: 0.12, ease: 'easeOut' }}
                    role="tooltip"
                >
                    <div
                        className="tooltip-arrow"
                        style={{ left: coords.arrowLeft }}
                    />
                    {content}
                </motion.div>
            )}
        </AnimatePresence>
    );

    return (
        <>
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
            </span>
            {createPortal(tooltipElement, document.body)}
        </>
    );
}

export default Tooltip;

