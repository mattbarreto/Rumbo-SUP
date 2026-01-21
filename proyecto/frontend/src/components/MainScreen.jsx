import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useSpring, animated } from 'react-spring';
import { useDrag } from 'react-use-gesture';
import { triggerHaptic } from '../utils/haptics';
import { useUserProfile } from '../hooks/useUserProfile';
import { useStaggeredReveal } from '../hooks/useStaggeredReveal';
import { getTimeline } from '../services/api';
import CircularIndicator from './CircularIndicator';
import WindVisualizer from './WindVisualizer';
import TimelineWidget from './TimelineWidget';
import SessionGoalSelector from './SessionGoalSelector';
import MetricCard from './MetricCard';
import metricCard from './MetricCard';
import Tooltip from './Tooltip';
import { WindIcon, WaveIcon, TideIcon, RefreshIcon, SettingsIcon, BrainIcon, LocationIcon, TimeIcon, ShieldIcon, EffortIcon, EnjoymentIcon, AlertIcon, ShareIcon } from './Icons';
import { WindIconMinimal, DirectionIconMinimal, WaveIconMinimal, UpdateIconMinimal, BrainIconMinimal, ShieldIconMinimal, EffortIconMinimal, EnjoymentIconMinimal } from './WeatherIcons';
import RumboPanel from './RumboPanel';
import OceanSkeleton from './OceanSkeleton';
import ColdStartLoader from './ColdStartLoader';
import BackgroundOcean from './BackgroundOcean';
import { getWindSafetyInfo } from '../utils/windUtils';
import './MainScreen.css';

function MainScreen() {
    const navigate = useNavigate();
    const { profile, updateProfile } = useUserProfile();
    // Animation container ref
    const containerRef = useStaggeredReveal({ delay: 200, interval: 80 });

    const [sessionGoal, setSessionGoal] = useState(profile?.session_goal || 'calma');
    const [timelineData, setTimelineData] = useState(null);
    const [selectedIndex, setSelectedIndex] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showColdStartLoader, setShowColdStartLoader] = useState(false);
    const [isRefreshing, setIsRefreshing] = useState(false);

    // Pull to Refresh Spring
    const [{ y }, api] = useSpring(() => ({ y: 0 }));

    // Pull to Refresh Gesture
    const bind = useDrag(({ down, movement: [, my], velocity, direction: [, yDir] }) => {
        // Only trigger if at top of page and pulling down
        if (window.scrollY === 0 && my > 0) {
            // Apply resistance
            const dampedY = down ? my / 2.5 : 0;
            api.start({ y: dampedY, immediate: down });

            // Trigger refresh on release if pulled far enough
            if (!down && my > 100 && !isRefreshing) {
                setIsRefreshing(true);
                handleRefresh().finally(() => {
                    setTimeout(() => setIsRefreshing(false), 500); // Visual delay
                });
            }
        }
    }, {
        filterTaps: true,
        bounds: { top: 0 },
        rubberband: true
    });

    // Generate a unique cache key based on critical parameters
    const getCacheKey = () => `rumbo_cache_varese_${sessionGoal}`;

    // ... existing loadData/fetchAnalysis/etc ... (implicitly preserved by tool, but I must match imports and start of function)
    // To minimize replacement size, I will target the imports and the return statement primarily, 
    // but the tool requires contiguous blocks.
    // I will replace the top imports and the start of the function, 
    // AND then a second replacement for the Return statement.
    // This tool call is for Imports + Component Start + Gesture Logic.

    useEffect(() => {
        if (profile) {
            loadData();
        }
    }, [profile, sessionGoal]);

    const loadData = async () => {
        const cacheKey = getCacheKey();
        const cached = sessionStorage.getItem(cacheKey);

        // 1. Try Cache First
        if (cached) {
            try {
                const { timestamp, data } = JSON.parse(cached);
                const ageMinutes = (Date.now() - timestamp) / (1000 * 60);

                if (ageMinutes < 30) {
                    console.log(`📦 Serving from cache (${Math.round(ageMinutes)}m old)`);
                    setTimelineData(data);
                    setSelectedIndex(0);
                    setLoading(false);
                    return;
                } else {
                    console.log('⌛ Cache expired, refetching...');
                }
            } catch (e) {
                console.warn('Cache parse error', e);
            }
        }

        // 2. Fetch Fresh Data
        await fetchAnalysis();
    };

    const fetchAnalysis = async () => {
        setLoading(true);
        setError(null);

        // Cold start detection: Show loader if request takes > 3 seconds
        const coldStartTimer = setTimeout(() => {
            setShowColdStartLoader(true);
        }, 3000);

        try {
            // Por ahora usamos Varese hardcoded
            const data = await getTimeline('varese', {
                ...profile,
                session_goal: sessionGoal
            });

            // Save to Cache
            sessionStorage.setItem(getCacheKey(), JSON.stringify({
                timestamp: Date.now(),
                data: data
            }));

            setTimelineData(data);
            setSelectedIndex(0); // Reset a "Ahora"
        } catch (err) {
            console.error('Error fetching timeline:', err);
            setError('No se pudieron obtener las condiciones. Verificá tu conexión.');
        } finally {
            clearTimeout(coldStartTimer);
            setShowColdStartLoader(false);
            setLoading(false);
        }
    };

    const handleGoalChange = (newGoal) => {
        setSessionGoal(newGoal);
        updateProfile({ session_goal: newGoal });
    };

    const handleRefresh = () => {
        triggerHaptic('medium');
        return fetchAnalysis();
    };

    // Calculate data freshness (fresh if < 1 hour old)
    const getFreshness = () => {
        if (!timelineData?.weather?.timestamp) return 'fresh';
        const dataTime = new Date(timelineData.weather.timestamp);
        const now = new Date();
        const diffHours = (now - dataTime) / (1000 * 60 * 60);
        return diffHours < 1 ? 'fresh' : 'stale';
    };

    const handlePointSelect = (point, index) => {
        setSelectedIndex(index);

        // Scroll to CircularIndicator (main result section) when timeline item is selected
        // Ensures the selected forecast is visible without the top being cut off
        setTimeout(() => {
            const circularIndicator = document.querySelector('.circular-indicator');
            if (circularIndicator) {
                const headerOffset = 120; // Main header + spot name + timeline title (~120px)
                const elementPosition = circularIndicator.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        }, 100); // Small delay to ensure DOM is updated
    };

    const handleShare = async () => {
        if (navigator.share) {
            try {
                await navigator.share({
                    title: 'Rumbo SUP',
                    text: 'Chequeá las condiciones en Varese para remar hoy!',
                    url: window.location.href,
                });
            } catch (error) {
                console.log('Error sharing:', error);
            }
        } else {
            alert('¡Enlace copiado al portapapeles!');
            navigator.clipboard.writeText(window.location.href);
        }
    };

    // Show cold start loader for Render.com wake-up
    if (showColdStartLoader) {
        return <ColdStartLoader />;
    }

    if (loading) {
        return (
            <div className="page main-screen">
                <OceanSkeleton />
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

    if (!timelineData) return null;

    // Derived State
    const spot = timelineData.spot;
    const currentPoint = timelineData.timeline[selectedIndex];
    const weather = currentPoint.weather;
    const result = currentPoint.result;

    // Safety: Calculate standardized wind info
    // IMPORTANTE: Usamos relative_direction del backend como fuente de verdad
    // para garantizar coherencia entre alertas y visualizadores
    const windInfo = getWindSafetyInfo(
        weather.wind.direction_deg,
        weather.wind.speed_kmh,
        'varese',
        weather.wind.relative_direction  // Del backend
    );


    // Si no es el primero, es futuro
    const isForecast = selectedIndex > 0;

    // Flags de alerta - tipo de alerta para el icono
    const flagVariants = {
        'viento_fuerte': 'warning',
        'riesgo_deriva': 'danger',
        'olas_grandes': 'warning',
        'principiante_condiciones_moderadas': 'warning',
        'deriva_varese': 'danger',
        'uv_alto': 'warning',
        'uv_extremo': 'danger'
    };

    const flagDescriptions = {
        'viento_fuerte': 'Viento fuerte',
        'riesgo_deriva': 'Riesgo de deriva',
        'olas_grandes': 'Olas grandes',
        'principiante_condiciones_moderadas': 'Condiciones moderadas para principiante',
        'deriva_varese': 'Marea bajando + viento offshore',
        'uv_alto': 'Índice UV Alto',
        'uv_extremo': 'Índice UV Extremo'
    };

    const flagTooltips = {
        'viento_fuerte': 'Vientos superiores a 25 km/h dificultan el control y aumentan el esfuerzo físico.',
        'riesgo_deriva': 'Condiciones que pueden alejarte de tu posición original (corrientes, viento offshore).',
        'olas_grandes': 'Olas que requieren técnica avanzada de equilibrio y mayor consumo energético.',
        'principiante_condiciones_moderadas': 'Si recién empezás, estas condiciones podrían ser desafiantes.',
        'deriva_varese': 'Combinación peligrosa: marea bajante + viento offshore = alto riesgo de alejamiento.',
        'uv_alto': 'Protección solar necesaria. Riesgo de quemaduras en exposición prolongada.',
        'uv_extremo': 'Evitar exposición directa. Protección solar máxima requerida.'
    };

    return (
        <motion.div
            className="page"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{
                type: 'spring',
                stiffness: 300,
                damping: 30
            }}
        >
            {/* Dynamic Background */}
            <BackgroundOcean
                windSpeed={weather.wind.speed_kmh}
                safetyScore={result.scores.seguridad}
                waveHeight={weather.waves.height_m}
            />
            {/* Pull to Refresh Wrapper */}
            <animated.div
                {...bind()}
                style={{ y, touchAction: 'pan-y' }}
                className="main-screen"
            >
                {/* Refresh Indicator (Visible on pull) */}
                <animated.div
                    style={{
                        opacity: y.to([0, 60], [0, 1]),
                        height: 0,
                        overflow: 'visible',
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        transform: y.to(v => `translateY(${v < 50 ? -50 : v / 2 - 50}px)`)
                    }}
                >
                    <div className={`pull-refresh-loader ${isRefreshing ? 'refreshing' : ''}`} style={{
                        marginTop: '-40px',
                        background: 'var(--ocean-surface)',
                        padding: '8px 16px',
                        borderRadius: '20px',
                        color: 'var(--ocean-cyan)',
                        fontSize: '12px',
                        fontWeight: 'bold',
                        boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        border: '1px solid rgba(64, 224, 208, 0.3)'
                    }}>
                        <UpdateIconMinimal size={16} className={isRefreshing ? 'spin' : ''} />
                        {isRefreshing ? 'Actualizando...' : 'Soltá para actualizar'}
                    </div>
                </animated.div>

                <div className="container" ref={containerRef}>
                    {/* Header */}
                    <div className="main-header">
                        <div>
                            <h1 className="spot-name">{spot.name}</h1>
                            <p className="spot-subtitle">
                                <LocationIcon size={16} />
                                <span>Mar del Plata</span>
                                <span className="separator">•</span>
                                <TimeIcon size={16} />
                                <span className={isForecast ? 'highlight-time' : ''}>
                                    {isForecast ? `Pronóstico ${currentPoint.hour_label}` : 'Ahora'}
                                </span>
                            </p>
                        </div>
                        <div className="header-actions">
                            <motion.button
                                className="btn-icon"
                                onClick={handleShare}
                                aria-label="Compartir"
                                whileTap={{ scale: 0.95 }}
                            >
                                <ShareIcon size={20} />
                            </motion.button>
                            <motion.button
                                className="btn-icon"
                                onClick={() => navigate('/profile')}
                                aria-label="Configuración"
                                whileTap={{ scale: 0.95 }}
                            >
                                <SettingsIcon size={20} />
                            </motion.button>
                        </div>
                    </div>

                    {/* Banner de Pronóstico */}
                    {isForecast && (
                        <div className="forecast-banner fade-in-up">
                            Viendo condiciones futuras ({currentPoint.hour_label})
                        </div>
                    )}

                    {/* Flags de Alerta - Moved to Top for Visibility */}
                    {result.flags && result.flags.length > 0 && (
                        <div className="alerts-section">
                            {result.flags.map(flag => (
                                <div key={flag} className={`alert ${flagVariants[flag] === 'danger' ? 'alert-danger' : 'alert-warning'} `}>
                                    <AlertIcon size={18} variant={flagVariants[flag] || 'warning'} />
                                    <Tooltip content={flagTooltips[flag] || 'Condición que requiere atención.'}>
                                        <span className="alert-text term-highlight">{flagDescriptions[flag] || flag}</span>
                                    </Tooltip>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Hero Zone: Safety First */}
                    <section className="hero-zone">
                        {/* Indicador Circular de SEGURIDAD */}
                        <CircularIndicator
                            seguridad={result.scores.seguridad}
                            categoria={result.categories.seguridad}
                            freshness={getFreshness()}
                        />
                    </section>

                    {/* Context Zone: Details */}
                    <section className="context-zone">

                        {/* LAYER A: Raw Conditions - Industrial Safety Cockpit */}
                        <section className="layer-a-section">
                            <h3 className="section-title">Condiciones</h3>
                            <div className="metrics-grid metrics-grid--layer-a">
                                <MetricCard
                                    label="Viento"
                                    value={weather.wind.speed_kmh !== null ? Math.round(weather.wind.speed_kmh) : null}
                                    unit="km/h"
                                    icon={<WindIconMinimal size={24} />}
                                    threshold="wind"
                                />
                                <MetricCard
                                    label="Dirección"
                                    value={windInfo.abbr}
                                    unit=""
                                    icon={<DirectionIconMinimal size={24} style={{ transform: `rotate(${windInfo.degrees}deg)` }} />}
                                    threshold={null}
                                />
                                <MetricCard
                                    label="Olas"
                                    value={weather.waves.height_m !== null ? weather.waves.height_m.toFixed(1) : null}
                                    unit="m"
                                    icon={<WaveIconMinimal size={24} />}
                                    threshold="wave"
                                />
                            </div>
                        </section>

                        {/* LAYER B: Analysis & Interpretation */}
                        <section className="layer-b-section">
                            <h3 className="section-title">Análisis</h3>
                            <div className="metrics-grid metrics-grid--layer-b">
                                <MetricCard
                                    label="Seguridad"
                                    value={result.scores.seguridad}
                                    unit="%"
                                    icon={<ShieldIconMinimal size={24} />}
                                    threshold={null}
                                />
                                <MetricCard
                                    label="Esfuerzo"
                                    value={result.scores.esfuerzo}
                                    unit="%"
                                    icon={<EffortIconMinimal size={24} />}
                                    threshold={null}
                                />
                                <MetricCard
                                    label="Disfrute"
                                    value={result.scores.disfrute}
                                    unit="%"
                                    icon={<EnjoymentIconMinimal size={24} />}
                                    threshold={null}
                                />
                            </div>
                        </section>

                        {/* Timeline Widget */}
                        <TimelineWidget
                            timeline={timelineData.timeline}
                            onPointSelect={handlePointSelect}
                            selectedIndex={selectedIndex}
                        />

                        {/* Wind Visualizer (Windy-like) */}
                        <div style={{ height: '120px', overflow: 'hidden', borderRadius: 'var(--radius-lg)', marginBottom: 'var(--space-4)' }}>
                            <WindVisualizer
                                speed={weather.wind.speed_kmh}
                                direction={weather.wind.direction_deg}
                                relativeDirection={windInfo.relativeDirection}
                            />
                        </div>
                    </section>

                    {/* Selector de Objetivo - Below Fold */}
                    {!isForecast && (
                        <SessionGoalSelector
                            value={sessionGoal}
                            onChange={handleGoalChange}
                        />
                    )}

                    {/* Condiciones Detalladas */}
                    <div className="card conditions-card">
                        <h3>Detalles {isForecast ? `(${currentPoint.hour_label})` : ''}</h3>
                        <div className="conditions-grid">
                            <div className="condition-item">
                                <WindIcon className="condition-icon" size={24} />
                                <div className="condition-label">Viento</div>
                                <div className="condition-value">
                                    {weather.wind.speed_kmh !== null ? `${weather.wind.speed_kmh} km/h` : '- km/h'}
                                </div>
                                <div className="condition-details">
                                    <span className="text-sm text-secondary" style={{ textAlign: 'right' }}>
                                        {windInfo.fromToLabel}
                                    </span>
                                    {windInfo.relativeDirection === 'onshore' && (
                                        <Tooltip content="Viento que sopla desde el mar hacia la playa. Ayuda a volver a la costa.">
                                            <span className="term-highlight status-onshore">→ Playa (onshore)</span>
                                        </Tooltip>
                                    )}
                                    {windInfo.relativeDirection === 'offshore' && (
                                        <Tooltip content="Viento que sopla desde la playa hacia el mar. Puede alejarte de la costa - mayor riesgo.">
                                            <span className="term-highlight status-offshore">→ Mar (offshore)</span>
                                        </Tooltip>
                                    )}
                                    {windInfo.relativeDirection === 'cross' && (
                                        <Tooltip content="Viento paralelo a la costa. Deriva lateral - mantené referencia visual.">
                                            <span className="term-highlight">↔ Paralelo (cross)</span>
                                        </Tooltip>
                                    )}
                                </div>
                            </div>
                            <div className="condition-item">
                                <WaveIcon className="condition-icon" size={24} />
                                <div className="condition-label">Olas</div>
                                <div className="condition-value">{weather.waves.height_m !== null ? `${weather.waves.height_m}m` : '- m'}</div>
                            </div>
                            <div className="condition-item">
                                <TideIcon className="condition-icon" size={24} direction={weather.tide.state} />
                                <div className="condition-label">Marea</div>
                                <div className="condition-value">
                                    {weather.tide.state === 'rising' ? 'Subiendo' : weather.tide.state === 'falling' ? 'Bajando' : weather.tide.state === 'high' ? 'Alta' : 'Baja'}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Acciones */}
                    <div className="actions-section">
                        {!isForecast && (
                            <motion.button
                                className="btn btn-primary btn-large btn-wave"
                                onClick={handleRefresh}
                                whileTap={{ scale: 0.95, y: 2 }}
                                transition={{ duration: 0.1 }}
                            >
                                <UpdateIconMinimal size={20} style={{ marginRight: '8px' }} /> Actualizar
                            </motion.button>
                        )}
                        <motion.button
                            className="btn btn-secondary btn-large"
                            onClick={() => navigate('/sensei', {
                                state: { user: profile, weather, result }
                            })}
                            whileTap={{ scale: 0.95, y: 2 }}
                            transition={{ duration: 0.1 }}
                        >
                            <BrainIconMinimal size={20} style={{ marginRight: '8px' }} /> Análisis del Guía
                        </motion.button>
                    </div>
                </div>
            </animated.div>
        </motion.div>
    );
}

export default MainScreen;
