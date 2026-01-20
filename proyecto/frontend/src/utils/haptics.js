/**
 * Trigger haptic feedback (Vibration API)
 * Tipos: light, medium, heavy, error, success
 */
export function triggerHaptic(type = 'light') {
    // Silent fail if Vibration API is not supported
    if (typeof navigator === 'undefined' || !navigator.vibrate) return;

    const patterns = {
        light: 10,                      // Tap suave (10ms) - UI interactions
        medium: 25,                     // Tap medio (25ms) - Important actions
        heavy: 50,                      // Tap fuerte (50ms) - Major events
        double: [10, 50, 10],           // Double tap - Notifications
        error: [20, 100, 20, 100, 20],  // Alerta - Errors
        success: [10, 50, 10, 50, 30]   // Confirmación - Completions
    };

    // Apply the pattern, defaulting to 'light' if type not found or if passing custom milliseconds
    try {
        // Prevent "Intervention" warnings by checking if user has interacted
        if (navigator.userActivation && !navigator.userActivation.hasBeenActive) {
            return;
        }

        const pattern = patterns[type] || (typeof type === 'number' ? type : patterns.light);
        navigator.vibrate(pattern);
    } catch (e) {
        // Ignore errors (some browsers restrict vibration without user interaction)
    }
}
