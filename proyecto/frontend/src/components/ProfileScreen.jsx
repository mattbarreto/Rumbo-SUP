import { useUserProfile } from '../hooks/useUserProfile';
import { useNavigate } from 'react-router-dom';
import { SettingsIcon, ShieldIcon, EffortIcon, EnjoymentIcon, WaveIcon } from './Icons';
import './ProfileScreen.css';

function ProfileScreen() {
    const { profile, clearProfile } = useUserProfile();
    const navigate = useNavigate();

    const handleReset = () => {
        if (confirm('¿Querés volver a hacer el onboarding?')) {
            // Force direct removal to avoid hook race conditions
            localStorage.removeItem('userProfile');
            clearProfile();
            // Force navigation to root
            window.location.href = '/';
        }
    };

    if (!profile) {
        return <div className="page"><div className="container"><p>Cargando...</p></div></div>;
    }

    const experienceLabels = {
        beginner: 'Principiante',
        intermediate: 'Intermedio',
        advanced: 'Avanzado'
    };

    const powerLabels = {
        low: 'Baja',
        medium: 'Media',
        high: 'Alta'
    };

    const goalLabels = {
        calma: 'Calma',
        entrenamiento: 'Entrenamiento',
        desafio: 'Desafío'
    };

    return (
        <div className="page profile-screen">
            <div className="container">
                <div className="profile-header">
                    <button className="btn-back-nav" onClick={() => navigate('/')}>
                        ← Atrás
                    </button>
                    <div className="profile-title">
                        <SettingsIcon size={24} className="profile-icon" />
                        <h1>Tu Perfil</h1>
                    </div>
                </div>

                <div className="profile-card">
                    <div className="profile-item">
                        <div className="profile-item-icon">
                            <WaveIcon size={20} />
                        </div>
                        <div className="profile-item-content">
                            <span className="profile-label">Tabla</span>
                            <span className="profile-value">
                                {profile.boardType === 'rigid' ? 'Rígida' : 'Inflable'}
                            </span>
                        </div>
                    </div>

                    <div className="profile-item">
                        <div className="profile-item-icon">
                            <ShieldIcon size={20} />
                        </div>
                        <div className="profile-item-content">
                            <span className="profile-label">Experiencia</span>
                            <span className="profile-value">
                                {experienceLabels[profile.experience] || profile.experience}
                            </span>
                        </div>
                    </div>

                    <div className="profile-item">
                        <div className="profile-item-icon">
                            <EffortIcon size={20} />
                        </div>
                        <div className="profile-item-content">
                            <span className="profile-label">Potencia de remada</span>
                            <span className="profile-value">
                                {powerLabels[profile.paddlePower] || profile.paddlePower}
                            </span>
                        </div>
                    </div>

                    <div className="profile-item">
                        <div className="profile-item-icon">
                            <EnjoymentIcon size={20} />
                        </div>
                        <div className="profile-item-content">
                            <span className="profile-label">Objetivo preferido</span>
                            <span className="profile-value">
                                {goalLabels[profile.sessionGoal] || profile.sessionGoal}
                            </span>
                        </div>
                    </div>
                </div>

                <div className="profile-actions">
                    <button className="btn btn-about" onClick={() => navigate('/about')}>
                        Acerca de Rumbo & Creador
                    </button>
                    <button className="btn btn-secondary" onClick={handleReset}>
                        Reiniciar Onboarding
                    </button>
                </div>
            </div>
        </div>
    );
}

export default ProfileScreen;
