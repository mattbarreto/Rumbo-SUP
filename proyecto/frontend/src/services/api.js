import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 90000, // 90 segundos para soportar cold start de Render
});

/**
 * Helper to map frontend profile (camelCase) to backend schema (snake_case)
 */
function mapProfileToBackend(profile) {
    if (!profile) return null;
    return {
        board_type: profile.boardType || profile.board_type, // Fallback for legacy
        experience: profile.experience,
        paddle_power: profile.paddlePower || profile.paddle_power,
        session_goal: profile.sessionGoal || profile.session_goal
    };
}

/**
 * Analiza condiciones para un spot y usuario
 */
export async function analyzeConditions(spotId, userProfile) {
    try {
        const response = await api.post('/api/analyze', {
            spot_id: spotId,
            user: mapProfileToBackend(userProfile)
        });
        return response.data;
    } catch (error) {
        console.error('Error analyzing conditions:', error);
        throw error;
    }
}

/**
 * Obtiene explicación pedagógica (Fase 3)
 */
export async function getExplanation(user, weather, result) {
    try {
        const response = await api.post('/api/pedagogy/explain', {
            user: mapProfileToBackend(user),
            weather,
            result
        });
        return response.data;
    } catch (error) {
        console.error('Error getting explanation:', error);
        throw error;
    }
}

/**
 * Obtiene el spot más cercano
 */
export async function getNearestSpot(lat, lon) {
    try {
        const response = await api.get('/api/spots/nearest', {
            params: { lat, lon }
        });
        return response.data;
    } catch (error) {
        console.error('Error getting nearest spot:', error);
        throw error;
    }
}

/**
 * Obtiene línea de tiempo semántica
 */
export async function getTimeline(spotId, userProfile) {
    try {
        const response = await api.post('/api/timeline', {
            spot_id: spotId,
            user: mapProfileToBackend(userProfile)
        });
        return response.data;
    } catch (error) {
        console.error('Error getting timeline:', error);
        throw error;
    }
}

/**
 * Health check del backend
 */
export async function healthCheck() {
    try {
        const response = await api.get('/api/health');
        return response.data;
    } catch (error) {
        console.error('Backend not available:', error);
        return null;
    }
}

export default api;
