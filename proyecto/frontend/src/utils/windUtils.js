/**
 * Wind Safety Utilities
 * Critical for user safety. Changes here must be verified against PROMPTS.md rules.
 */

const CARDINAL_DIRECTIONS = [
    "Norte", "Noreste", "Este", "Sureste",
    "Sur", "Suroeste", "Oeste", "Noroeste"
];

const CARDINAL_ABBR = [
    "N", "NE", "E", "SE",
    "S", "SO", "O", "NO"
];

/**
 * Converts meteorological degrees (0-360) to Cardinal Name.
 * 0/360 = North.
 * Step = 45 degrees.
 */
export function getCardinalName(degrees) {
    // Normalize to 0-360
    const normalized = (degrees % 360 + 360) % 360;
    // Offset by 22.5 to center the sectors (e.g. N is 337.5 - 22.5)
    // Math.round(deg / 45) works but handling the wraparound 8->0 is key.
    const index = Math.round(normalized / 45) % 8;
    return CARDINAL_DIRECTIONS[index];
}

export function getCardinalAbbr(degrees) {
    const normalized = (degrees % 360 + 360) % 360;
    const index = Math.round(normalized / 45) % 8;
    return CARDINAL_ABBR[index];
}

/**
 * Safety-critical calculation for Mar del Plata (Varese).
 * Coast orientation: Approximated as East-facing.
 * 
 * Logic defined by Safety Rule:
 * NNE (22.5) to SSE (157.5) -> Onshore (From Sea)
 * S (157.5) to SSW (202.5) -> Cross
 * SSW (202.5) to NNW (337.5) -> Offshore (From Land)
 * NNW (337.5) to NNE (22.5) -> Cross / Default (North is technically Cross-shore slightly On depending on beach curve)
 * 
 * User Spec:
 * deg >= 22.5 && deg <= 157.5) return 'onshore';
 * deg > 157.5 && deg < 202.5) return 'cross';
 * deg >= 202.5 && deg <= 337.5) return 'offshore';
 * return 'cross';
 */
export function calculateMarDelPlataOffshore(degrees) {
    const deg = (degrees % 360 + 360) % 360;

    if (deg >= 22.5 && deg <= 157.5) return 'onshore';
    if (deg > 157.5 && deg < 202.5) return 'cross';
    if (deg >= 202.5 && deg <= 337.5) return 'offshore';

    // 337.5 - 360 - 22.5 (North Sector)
    return 'cross';
}

/**
 * Get comprehensive wind safety info.
 * @param {number} degrees - Wind direction in degrees
 * @param {number} speed - Wind speed (unused for direction, but good for context)
 * @param {string} spotId - ID to choose strategy (currently hardcoded for MDP/Varese context)
 * @param {string|null} backendRelativeDirection - Optional value from backend to use as source of truth
 */
export function getWindSafetyInfo(degrees, speed, spotId = 'varese', backendRelativeDirection = null) {
    const cardinal = getCardinalName(degrees);
    const abbr = getCardinalAbbr(degrees);

    // Destination Name (Opposite)
    const destDegrees = (degrees + 180) % 360;
    const destCardinal = getCardinalName(destDegrees);

    // Safety Calculation
    // Si el backend provee un valor, lo usamos como fuente de verdad
    // Esto garantiza coherencia entre alertas y visualizadores
    const relativeDirection = backendRelativeDirection || calculateMarDelPlataOffshore(degrees);

    return {
        degrees,
        cardinal,
        abbr,
        cardinalLabel: `${cardinal} (${abbr})`,
        fromToLabel: `${cardinal} (${abbr}) → Hacia ${destCardinal}`,
        relativeDirection,
        isOffshore: relativeDirection === 'offshore',
        isOnshore: relativeDirection === 'onshore'
    };
}
