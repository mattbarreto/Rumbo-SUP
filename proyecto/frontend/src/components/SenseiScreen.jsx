import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { getExplanation } from '../services/api';
import ReactMarkdown from 'react-markdown';
import { BrainIcon } from './Icons';
import './SenseiScreen.css';

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
                        <p>Analizando condiciones con IA...</p>
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
                        <span>⚠️</span>
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
                        ← Atrás
                    </button>
                    <div className="sensei-brand">
                        <BrainIcon size={28} className="sensei-icon" />
                        <h1>Guía de Mar</h1>
                    </div>
                </div>

                {/* Explicación */}
                {explanation && (
                    <div className="explanation-card">
                        <div className="markdown-content">
                            <ReactMarkdown>
                                {explanation}
                            </ReactMarkdown>
                        </div>
                    </div>
                )}

                {/* Disclaimer */}
                <div className="sensei-footer">
                    <div className="disclaimer-badge">
                        <span className="disclaimer-icon">🤝</span>
                        <p>
                            Esto es para ayudarte a leer el mar, no para decidir por vos.
                            <br />
                            <strong>Confiá en lo que ves y en cómo te sentís antes de entrar.</strong>
                        </p>
                    </div>

                    <button className="btn btn-primary btn-large" onClick={() => navigate('/')}>
                        Entendido
                    </button>
                </div>
            </div>
        </div>
    );
}

export default SenseiScreen;
