import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUserProfile } from '../hooks/useUserProfile';
import { analyzeConditions } from '../services/api';
import CircularIndicator from './CircularIndicator';
import MetricCard from './MetricCard';
import SessionGoalSelector from './SessionGoalSelector';
import { WindIcon, WaveIcon, TideIcon, RefreshIcon, SettingsIcon, BrainIcon, LocationIcon, TimeIcon, ShieldIcon, EffortIcon, EnjoymentIcon, AlertIcon } from './Icons';
import './MainScreen.css';

function MainScreen() {
    const navigate = useNavigate();
    const { profile, updateProfile } = useUserProfile();
    const [sessionGoal, setSessionGoal] = useState(profile?.session_goal || 'calma');
    const [analysis, setAnalysis] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (profile) {
            fetchAnalysis();
        }
    }, [profile, sessionGoal]);

    const fetchAnalysis = async () => {
        setLoading(true);
        setError(null);

        try {
            // Por ahora usamos Varese hardcoded
            // En futuro: usar geolocalización + getNearestSpot
            const data = await analyzeConditions('varese', {
                ...profile,
                session_goal: sessionGoal
            });

            setAnalysis(data);
        } catch (err) {
            console.error('Error fetching analysis:', err);
            setError('No se pudieron obtener las condiciones. Verificá tu conexión.');
        } finally {
            setLoading(false);
        }
    };

    const handleGoalChange = (newGoal) => {
        setSessionGoal(newGoal);
        updateProfile({ session_goal: newGoal });
    };

    const handleRefresh = () => {
        fetchAnalysis();
    };

    if (loading) {
        return (
            <div className="page">
                <div className="container">
                    <div className="loading-container">
                        <div className="loading-spinner"></div>
                        <p>Obteniendo condiciones...</p>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="page">
                <div className="container">
                    <div className="alert alert-danger">
                        <span>⚠️</span>
                        <div>
                            <strong>Error</strong>
                            <p>{error}</p>
                        </div>
                    </div>
                    <button className="btn btn-primary" onClick={handleRefresh}>
                        Reintentar
                    </button>
                </div>
            </div>
        );
    }

    if (!analysis) return null;

    const { spot, weather, result } = analysis;

    // Flags de alerta - tipo de alerta para el icono
    const flagVariants = {
        'viento_fuerte': 'warning',
        'riesgo_deriva': 'danger',
        'olas_grandes': 'warning',
        'principiante_condiciones_moderadas': 'warning',
        'deriva_varese': 'danger'
    };

    const flagDescriptions = {
        'viento_fuerte': 'Viento fuerte',
        'riesgo_deriva': 'Riesgo de deriva',
        'olas_grandes': 'Olas grandes',
        'principiante_condiciones_moderadas': 'Condiciones moderadas para principiante',
        'deriva_varese': 'Marea bajando + viento offshore'
    };

    return (
        <div className="page main-screen">
            <div className="container">
                {/* Header */}
                <div className="main-header">
                    <div>
                        <h1 className="spot-name">{spot.name}</h1>
                        <p className="spot-subtitle">
                            <LocationIcon size={16} />
                            <span>Mar del Plata</span>
                            <span className="separator">•</span>
                            <TimeIcon size={16} />
                            <span>Ahora</span>
                        </p>
                    </div>
                    <button className="btn-icon" onClick={() => navigate('/profile')}>
                        <SettingsIcon size={20} />
                    </button>
                </div>

                {/* Selector de Objetivo */}
                <SessionGoalSelector
                    value={sessionGoal}
                    onChange={handleGoalChange}
                />

                {/* Indicador Circular de SEGURIDAD */}
                <CircularIndicator
                    seguridad={result.scores.seguridad}
                    categoria={result.categories.seguridad}
                />

                {/* Flags de Alerta */}
                {result.flags && result.flags.length > 0 && (
                    <div className="alerts-section">
                        {result.flags.map(flag => (
                            <div key={flag} className={`alert ${flagVariants[flag] === 'danger' ? 'alert-danger' : 'alert-warning'}`}>
                                <AlertIcon size={18} variant={flagVariants[flag] || 'warning'} />
                                <span>{flagDescriptions[flag] || flag}</span>
                            </div>
                        ))}
                    </div>
                )}

                {/* Métricas Separadas */}
                <div className="metrics-grid">
                    <MetricCard
                        label="Seguridad"
                        score={result.scores.seguridad}
                        categoria={result.categories.seguridad}
                        icon={<ShieldIcon size={18} />}
                    />
                    <MetricCard
                        label="Esfuerzo"
                        score={result.scores.esfuerzo}
                        categoria={result.categories.esfuerzo}
                        icon={<EffortIcon size={18} />}
                    />
                    <MetricCard
                        label="Disfrute"
                        score={result.scores.disfrute}
                        categoria={result.categories.disfrute}
                        icon={<EnjoymentIcon size={18} />}
                    />
                </div>

                {/* Condiciones Actuales */}
                <div className="card conditions-card">
                    <h3>Condiciones Actuales</h3>
                    <div className="conditions-grid">
                        <div className="condition-item">
                            <WindIcon className="condition-icon" size={32} />
                            <div>
                                <div className="condition-label">Viento</div>
                                <div className="condition-value">
                                    {weather.wind.speed_kmh} km/h {weather.wind.relative_direction === 'onshore' ? '→ Playa' : weather.wind.relative_direction === 'offshore' ? '→ Mar' : '↔ Paralelo'}
                                </div>
                            </div>
                        </div>
                        <div className="condition-item">
                            <WaveIcon className="condition-icon" size={32} />
                            <div>
                                <div className="condition-label">Olas</div>
                                <div className="condition-value">{weather.waves.height_m}m</div>
                            </div>
                        </div>
                        <div className="condition-item">
                            <TideIcon className="condition-icon" size={32} direction={weather.tide.state} />
                            <div>
                                <div className="condition-label">Marea</div>
                                <div className="condition-value">
                                    {weather.tide.state === 'rising' ? 'Subiendo' : weather.tide.state === 'falling' ? 'Bajando' : weather.tide.state === 'high' ? 'Alta' : 'Baja'}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Confianza del Modelo */}
                {result.confidence === 'baja' && (
                    <div className="alert alert-warning">
                        <span>ℹ️</span>
                        <div>
                            <strong>Confianza baja</strong>
                            <p>Los datos pueden estar desactualizados o incompletos</p>
                        </div>
                    </div>
                )}

                {/* Acciones */}
                <div className="actions-section">
                    <button className="btn btn-primary btn-large" onClick={handleRefresh}>
                        🔄 Actualizar
                    </button>
                    <button
                        className="btn btn-secondary btn-large"
                        onClick={() => navigate('/sensei', {
                            state: { user: profile, weather, result }
                        })}
                    >
                        🧠 ¿Por qué?
                    </button>
                </div>
            </div>
        </div>
    );
}

export default MainScreen;
