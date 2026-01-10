/**
 * Detecta si el dispositivo es móvil o tablet
 * @returns {boolean} true si es móvil/tablet, false si es desktop
 */
export function isMobile() {
    // Verificar por User Agent
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;

    const mobileRegex = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i;
    const isMobileUA = mobileRegex.test(userAgent.toLowerCase());

    // Verificar por tamaño de pantalla (backup)
    const isSmallScreen = window.innerWidth <= 768;

    // Verificar touch capability
    const hasTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

    // Retornar true si cumple al menos 2 condiciones
    const conditions = [isMobileUA, isSmallScreen, hasTouch];
    const trueCount = conditions.filter(Boolean).length;

    return trueCount >= 2;
}

/**
 * Verifica si hay modo desarrollo activado (para testing en desktop)
 * @returns {boolean}
 */
export function isDevMode() {
    return localStorage.getItem('devMode') === 'true';
}
