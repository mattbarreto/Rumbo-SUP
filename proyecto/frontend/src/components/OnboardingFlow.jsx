import { useState } from 'react';
import { motion } from 'framer-motion';
import { useUserProfile } from '../hooks/useUserProfile';
import { WaveIcon, LocationIcon, BrainIcon, EnjoymentIcon, EffortIcon, ShieldIcon, TargetIcon, TideIcon, BodyIcon } from './Icons';
import './OnboardingFlow.css';

function OnboardingFlow({ onComplete }) {
    const { saveProfile } = useUserProfile();
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        boardType: '',
        experience: '',
        paddlePower: '',
        sessionGoal: 'calma'
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
        if (step === 2) return formData.boardType && formData.experience && formData.paddlePower;
        if (step === 3) return formData.sessionGoal;
        return false;
    };

    return (
        <motion.div
            className="page onboarding-flow onboarding-page"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{
                type: 'spring',
                stiffness: 300,
                damping: 30
            }}
        >
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
                        <motion.button
                            className="btn btn-primary btn-large btn-wave"
                            onClick={handleNext}
                            whileTap={{ scale: 0.95, y: 2 }}
                            transition={{ duration: 0.1 }}
                        >
                            Comenzar
                        </motion.button>
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
                                    className={`radio-btn ${formData.boardType === 'rigid' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('boardType', 'rigid')}
                                >
                                    <ShieldIcon size={20} className="radio-icon" />
                                    <div className="radio-content">
                                        <span>Rígida</span>
                                        <small>Más estable en el agua</small>
                                    </div>
                                </button>
                                <button
                                    className={`radio-btn ${formData.boardType === 'inflable' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('boardType', 'inflable')}
                                >
                                    <BodyIcon size={20} className="radio-icon" />
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
                                    <TideIcon size={20} className="radio-icon" direction="falling" />
                                    <div className="radio-content">
                                        <span>Principiante</span>
                                        <small>Menos de 10 salidas</small>
                                    </div>
                                </button>
                                <button
                                    className={`radio-btn ${formData.experience === 'intermediate' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('experience', 'intermediate')}
                                >
                                    <TideIcon size={20} className="radio-icon" direction="neutral" />
                                    <div className="radio-content">
                                        <span>Intermedio</span>
                                        <small>Entre 10 y 50 salidas</small>
                                    </div>
                                </button>
                                <button
                                    className={`radio-btn ${formData.experience === 'advanced' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('experience', 'advanced')}
                                >
                                    <TideIcon size={20} className="radio-icon" direction="rising" />
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
                                    className={`radio-btn ${formData.paddlePower === 'low' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('paddlePower', 'low')}
                                >
                                    <TideIcon size={20} className="radio-icon" direction="falling" />
                                    <div className="radio-content">
                                        <span>Baja</span>
                                        <small>Me canso rápido</small>
                                    </div>
                                </button>
                                <button
                                    className={`radio-btn ${formData.paddlePower === 'medium' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('paddlePower', 'medium')}
                                >
                                    <TideIcon size={20} className="radio-icon" direction="neutral" />
                                    <div className="radio-content">
                                        <span>Media</span>
                                        <small>Resistencia normal</small>
                                    </div>
                                </button>
                                <button
                                    className={`radio-btn ${formData.paddlePower === 'high' ? 'active' : ''}`}
                                    onClick={() => handleInputChange('paddlePower', 'high')}
                                >
                                    <TideIcon size={20} className="radio-icon" direction="rising" />
                                    <div className="radio-content">
                                        <span>Alta</span>
                                        <small>Puedo remar contra viento</small>
                                    </div>
                                </button>
                            </div>
                        </div>

                        <div className="button-group">
                            <motion.button
                                className="btn btn-secondary"
                                onClick={() => setStep(1)}
                                whileTap={{ scale: 0.95, y: 2 }}
                                transition={{ duration: 0.1 }}
                            >
                                Atrás
                            </motion.button>
                            <motion.button
                                className="btn btn-primary btn-wave"
                                onClick={handleNext}
                                disabled={!canProceed()}
                                whileTap={{ scale: 0.95, y: 2 }}
                                transition={{ duration: 0.1 }}
                            >
                                Continuar
                            </motion.button>
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
                                className={`goal-card ${formData.sessionGoal === 'calma' ? 'active' : ''}`}
                                onClick={() => handleInputChange('sessionGoal', 'calma')}
                            >
                                <div className="goal-icon">
                                    <EnjoymentIcon size={36} />
                                </div>
                                <h3>Calma</h3>
                                <p>Busco relajarme y disfrutar del mar tranquilo</p>
                            </button>

                            <button
                                className={`goal-card ${formData.sessionGoal === 'entrenamiento' ? 'active' : ''}`}
                                onClick={() => handleInputChange('sessionGoal', 'entrenamiento')}
                            >
                                <div className="goal-icon">
                                    <EffortIcon size={36} />
                                </div>
                                <h3>Entrenamiento</h3>
                                <p>Quiero mejorar mi técnica y condición física</p>
                            </button>

                            <button
                                className={`goal-card ${formData.sessionGoal === 'desafio' ? 'active' : ''}`}
                                onClick={() => handleInputChange('sessionGoal', 'desafio')}
                            >
                                <div className="goal-icon">
                                    <WaveIcon size={36} />
                                </div>
                                <h3>Desafío</h3>
                                <p>Busco condiciones exigentes y emociones fuertes</p>
                            </button>
                        </div>

                        <div className="button-group">
                            <motion.button
                                className="btn btn-secondary"
                                onClick={() => setStep(2)}
                                whileTap={{ scale: 0.95, y: 2 }}
                                transition={{ duration: 0.1 }}
                            >
                                Atrás
                            </motion.button>
                            <motion.button
                                className="btn btn-primary btn-wave"
                                onClick={handleComplete}
                                whileTap={{ scale: 0.95, y: 2 }}
                                transition={{ duration: 0.1 }}
                            >
                                ¡Empezar!
                            </motion.button>
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
        </motion.div>
    );
}

export default OnboardingFlow;
