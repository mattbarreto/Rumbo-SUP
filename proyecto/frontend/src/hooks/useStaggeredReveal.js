import { useEffect, useRef } from 'react';

/**
 * Hook to apply a 'visible' class to child elements in a staggered sequence.
 * 
 * @param {Object} options Configuration options
 * @param {string} options.selector Selector for child elements to animate (default: '> *')
 * @param {number} options.delay Base delay in ms before starting (default: 100)
 * @param {number} options.interval Interval in ms between each element (default: 100)
 * @returns {React.RefObject} Ref to attach to the parent container
 */
export const useStaggeredReveal = ({ selector = '> *', delay = 100, interval = 100 } = {}) => {
    const parentRef = useRef(null);

    useEffect(() => {
        const parent = parentRef.current;
        if (!parent) return;

        // Select elements based on direct children or custom selector
        // If selector is distinct, find descendants. If default, map children.
        const elements = selector === '> *'
            ? Array.from(parent.children)
            : Array.from(parent.querySelectorAll(selector));

        // Reset opacity initially (assumes CSS handles this state)
        elements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(10px)';
            el.style.transition = 'opacity 0.5s cubic-bezier(0.2, 0.8, 0.2, 1), transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1)';
        });

        const timeouts = [];

        // Stagger loop
        elements.forEach((el, index) => {
            const timeout = setTimeout(() => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, delay + (index * interval));
            timeouts.push(timeout);
        });

        // Cleanup
        return () => {
            timeouts.forEach(t => clearTimeout(t));
            elements.forEach(el => {
                // Optional: remove inline styles on cleanup if unmounting
                // el.style.opacity = '';
                // el.style.transform = '';
            });
        };
    }, [selector, delay, interval]);

    return parentRef;
};
