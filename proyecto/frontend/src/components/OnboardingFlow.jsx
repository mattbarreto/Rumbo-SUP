import { useState } from 'react';
import { useUserProfile } from '../hooks/useUserProfile';
import { WaveIcon, LocationIcon, BrainIcon, EnjoymentIcon, EffortIcon, ShieldIcon } from './Icons';
import './OnboardingFlow.css';

function OnboardingFlow({ onComplete }) {
    const { saveProfile } = useUserProfile();
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        board_type: '',
        experience: '',
        paddle_power: '',
        session_goal: 'calma'
    });

    const handleInputChange = (field, value) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    const handleNext = () => {
        if (step < 3) {
            setStep(step + 1);
        } else {
            handleComplete();
        }
    };

    const handleComplete = () => {
        const success = saveProfile(formData);
        if (success) {
            onComplete();
        }
    };

    const canProceed = () => {
        if (step === 1) return true;
        if (step === 2) return formData.board_type && formData.experience && formData.paddle_power;
        if (step === 3) return formData.session_goal;
        return false;
    };

    return (
        <div className="onboarding-page">
            <div className="onboarding-container">

                {/* Step 1: Bienvenida */}
                {step === 1 && (
                    <div className="onboarding-step fade-in">
                        <div className="logo-container">
                            <div className="logo-brand">
                                <WaveIcon size={40} className="logo-icon" />
                                <h1 className="logo-text">Rumbo SUP</h1>
                            </div>
                        </div>
                        <h2>Tu Guía de Mar</h2>
                        <p className="subtitle">
                            Te ayudo a leer el mar y decidir cuándo es seguro entrar al agua.
                        </p>
                        <div className="feature-list">
                            <div className="feature-item">
                                <WaveIcon size={24} className="feature-icon" />
                                <span>Análisis de condiciones en tiempo real</span>
                            </div>
                            <div className="feature-item">
                                <LocationIcon size={24} className="feature-icon" />
                                <span>Recomendaciones para tu spot</span>
                            </div>
                            <div className="feature-item">
                                <BrainIcon size={24} className="feature-icon" />
                                <span>Explicaciones que te enseñan a leer el mar</span>
                            </div>
                        </div>
                        <button className="btn btn-primary btn-large" onClick={handleNext}>
                            Comenzar
                        </button>
                    </div>
                )}

                {/* Step 2: Perfil de Usuario */}
                {step === 2 && (
                    <div className="onboarding-step fade-in">
                        <h2>Tu Perfil</h2>
                        <p className="subtitle">
                            Contame sobre vos para personalizar las recomendaciones
                        </p>

                        <div className="form-group">
                            <label>Tipo de Tabla</label>
                            <div className="radio-group">
                                <button
                                    className={`radio-btn ${formData.board_type === 'rigid' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('board_type', 'rigid')}
                                >
                                    <ShieldIcon size={20} className="radio-icon" />
                                    <div className="radio-content">
                                        <span>Rígida</span>
                                        <small>Más estable en el agua</small>
                                    </div>
                                </button>
                                <button
                                    className={`radio-btn ${formData.board_type === 'inflable' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('board_type', 'inflable')}
                                >
                                    <WaveIcon size={20} className="radio-icon" />
                                    <div className="radio-content">
                                        <span>Inflable</span>
                                        <small>Más fácil de transportar</small>
                                    </div>
                                </button>
                            </div>
                        </div>

                        <div className="form-group">
                            <label>Nivel de Experiencia</label>
                            <div className="radio-group">
                                <button
                                    className={`radio-btn ${formData.experience === 'beginner' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('experience', 'beginner')}
                                >
                                    <div className="radio-content">
                                        <span>Principiante</span>
                                        <small>Menos de 10 salidas</small>
                                    </div>
                                </button>
                                <button
                                    className={`radio-btn ${formData.experience === 'intermediate' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('experience', 'intermediate')}
                                >
                                    <div className="radio-content">
                                        <span>Intermedio</span>
                                        <small>Entre 10 y 50 salidas</small>
                                    </div>
                                </button>
                                <button
                                    className={`radio-btn ${formData.experience === 'advanced' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('experience', 'advanced')}
                                >
                                    <div className="radio-content">
                                        <span>Avanzado</span>
                                        <small>Más de 50 salidas</small>
                                    </div>
                                </button>
                            </div>
                        </div>

                        <div className="form-group">
                            <label>Potencia de Remada</label>
                            <div className="radio-group">
                                <button
                                    className={`radio-btn ${formData.paddle_power === 'low' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('paddle_power', 'low')}
                                >
                                    <EffortIcon size={20} className="radio-icon" />
                                    <div className="radio-content">
                                        <span>Baja</span>
                                        <small>Me canso rápido</small>
                                    </div>
                                </button>
                                <button
                                    className={`radio-btn ${formData.paddle_power === 'medium' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('paddle_power', 'medium')}
                                >
                                    <EffortIcon size={20} className="radio-icon" />
                                    <div className="radio-content">
                                        <span>Media</span>
                                        <small>Resistencia normal</small>
                                    </div>
                                </button>
                                <button
                                    className={`radio-btn ${formData.paddle_power === 'high' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('paddle_power', 'high')}
                                >
                                    <EffortIcon size={20} className="radio-icon" />
                                    <div className="radio-content">
                                        <span>Alta</span>
                                        <small>Puedo remar contra viento</small>
                                    </div>
                                </button>
                            </div>
                        </div>

                        <div className="button-group">
                            <button className="btn btn-secondary" onClick={() => setStep(1)}>
                                Atrás
                            </button>
                            <button
                                className="btn btn-primary"
                                onClick={handleNext}
                                disabled={!canProceed()}
                            >
                                Continuar
                            </button>
                        </div>
                    </div>
                )}

                {/* Step 3: Objetivo de Sesión */}
                {step === 3 && (
                    <div className="onboarding-step fade-in">
                        <h2>¿Qué buscás hoy?</h2>
                        <p className="subtitle">
                            Esto afecta cómo calculamos tu disfrute. Podés cambiarlo en cada sesión.
                        </p>

                        <div className="goal-cards">
                            <button
                                className={`goal-card ${formData.session_goal === 'calma' ? 'active' : ''}`}
                                onClick={() => handleInputChange('session_goal', 'calma')}
                            >
                                <div className="goal-icon">
                                    <EnjoymentIcon size={36} />
                                </div>
                                <h3>Calma</h3>
                                <p>Busco relajarme y disfrutar del mar tranquilo</p>
                            </button>

                            <button
                                className={`goal-card ${formData.session_goal === 'entrenamiento' ? 'active' : ''}`}
                                onClick={() => handleInputChange('session_goal', 'entrenamiento')}
                            >
                                <div className="goal-icon">
                                    <EffortIcon size={36} />
                                </div>
                                <h3>Entrenamiento</h3>
                                <p>Quiero mejorar mi técnica y condición física</p>
                            </button>

                            <button
                                className={`goal-card ${formData.session_goal === 'desafio' ? 'active' : ''}`}
                                onClick={() => handleInputChange('session_goal', 'desafio')}
                            >
                                <div className="goal-icon">
                                    <WaveIcon size={36} />
                                </div>
                                <h3>Desafío</h3>
                                <p>Busco condiciones exigentes y emociones fuertes</p>
                            </button>
                        </div>

                        <div className="button-group">
                            <button className="btn btn-secondary" onClick={() => setStep(2)}>
                                Atrás
                            </button>
                            <button
                                className="btn btn-primary"
                                onClick={handleComplete}
                            >
                                ¡Empezar!
                            </button>
                        </div>
                    </div>
                )}

                {/* Progress Indicator */}
                <div className="progress-dots">
                    {[1, 2, 3].map(i => (
                        <span key={i} className={`dot ${step >= i ? 'active' : ''}`} />
                    ))}
                </div>
            </div>
        </div>
    );
}

export default OnboardingFlow;
