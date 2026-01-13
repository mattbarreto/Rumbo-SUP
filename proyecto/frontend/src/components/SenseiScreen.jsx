import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { getExplanation } from '../services/api';
import ReactMarkdown from 'react-markdown';
import {
    BrainIcon, AlertIcon, ArrowLeftIcon, InfoIcon,
    WaveIcon, SeeIcon, BodyIcon, IdeaIcon, TargetIcon
} from './Icons';
import './SenseiScreen.css';

// Componente para renderizar H2 con iconos dinámicos
const CustomH2 = ({ children, ...props }) => {
    // Obtener texto plano del título
    const text = String(children).toLowerCase();

    // Determinar icono basado en palabras clave
    let Icon = WaveIcon;
    let iconClass = "text-ocean-cyan";

    if (text.includes("mar") || text.includes("hoy")) {
        Icon = WaveIcon;
    } else if (text.includes("sentir") || text.includes("cuerpo")) {
        Icon = BodyIcon;
    } else if (text.includes("riesgo") || text.includes("evitar") || text.includes("alerta")) {
        Icon = AlertIcon;
    } else if (text.includes("visuales") || text.includes("mirar") || text.includes("ojos")) {
        Icon = SeeIcon;
    } else if (text.includes("plan") || text.includes("estrategia")) {
        Icon = IdeaIcon;
    } else if (text.includes("foco") || text.includes("practicando") || text.includes("aprendizaje")) {
        Icon = TargetIcon;
    }

    return (
        <div className="sensei-section-title">
            <Icon size={26} className={iconClass} />
            <h2 {...props}>{children}</h2>
        </div>
    );
};

function SenseiScreen() {
    const navigate = useNavigate();
    const location = useLocation();
    const [explanation, setExplanation] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Datos pasados desde MainScreen
    const { user, weather, result } = location.state || {};

    useEffect(() => {
        if (!user || !weather || !result) {
            navigate('/');
            return;
        }

        fetchExplanation();
    }, [user, weather, result, navigate]);

    const fetchExplanation = async () => {
        setLoading(true);
        setError(null);

        try {
            const data = await getExplanation(user, weather, result);
            setExplanation(data.explanation);
        } catch (err) {
            console.error('Error fetching explanation:', err);
            setError('No se pudo obtener la explicación');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="page sensei-screen">
                <div className="container">
                    <div className="loading-container">
                        <div className="loading-spinner"></div>
                        <p>Consultando al Guía...</p>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="page sensei-screen">
                <div className="container">
                    <div className="alert alert-danger">
                        <AlertIcon size={24} variant="danger" />
                        <div>
                            <strong>Error</strong>
                            <p>{error}</p>
                        </div>
                    </div>
                    <button className="btn btn-secondary" onClick={() => navigate('/')}>
                        Volver
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="page sensei-screen">
            <div className="container">
                {/* Header */}
                <div className="sensei-header">
                    <button className="btn-back-nav" onClick={() => navigate('/')}>
                        <ArrowLeftIcon size={20} />
                        <span>Atrás</span>
                    </button>
                    <div className="sensei-brand">
                        <BrainIcon size={28} className="text-ocean-cyan" />
                        <h1>Guía de Mar</h1>
                    </div>
                </div>

                {/* Explicación */}
                {explanation && (
                    <div className="explanation-card">
                        <div className="markdown-content">
                            <ReactMarkdown components={{ h2: CustomH2 }}>
                                {explanation}
                            </ReactMarkdown>
                        </div>
                    </div>
                )}

                {/* Disclaimer & Sponsor */}
                <div className="sensei-footer">
                    <div className="sponsor-slot">
                        <small>Potenciado por</small>
                        <div className="sponsor-placeholder">[ Tu Escuela de SUP ]</div>
                    </div>

                    <div className="disclaimer-badge">
                        <div className="disclaimer-icon-wrapper">
                            <InfoIcon size={20} className="text-ocean-shimmer" />
                        </div>
                        <p>
                            Rumbo es un asistente digital basado en datos.
                            <br />
                            <strong>No reemplaza a un instructor certificado.</strong> Consultá siempre a los locales.
                        </p>
                    </div>

                    <button className="btn btn-primary btn-large" onClick={() => navigate('/')}>
                        Volver al Inicio
                    </button>
                </div>
            </div>
        </div>
    );
}

export default SenseiScreen;
