import { useState } from 'react';
import { WaveIcon } from './Icons';
import './PasswordGate.css';

// SECURITY NOTE: This is a demo/beta access password for public repository
// In production, implement proper backend authentication with JWT tokens
const ACCESS_PASSWORD = 'supadmin';
const STORAGE_KEY = 'rumbo_access_v2'; // Bump version to force re-login

function PasswordGate({ children }) {
    const [isUnlocked, setIsUnlocked] = useState(() => {
        return localStorage.getItem(STORAGE_KEY) === 'true';
    });
    const [password, setPassword] = useState('');
    const [error, setError] = useState(false);
    const [shaking, setShaking] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();

        if (password === ACCESS_PASSWORD) {
            localStorage.setItem(STORAGE_KEY, 'true');
            setIsUnlocked(true);
        } else {
            setError(true);
            setShaking(true);
            setTimeout(() => setShaking(false), 500);
            setPassword('');
        }
    };

    if (isUnlocked) {
        return children;
    }

    return (
        <div className="password-gate">
            <div className={`password-card ${shaking ? 'shake' : ''}`}>
                <div className="password-logo">
                    <WaveIcon size={48} className="password-icon" />
                    <h1>Rumbo SUP</h1>
                </div>

                <p className="password-subtitle">
                    Beta privada - Acceso restringido
                </p>

                <form onSubmit={handleSubmit}>
                    <input
                        type="password"
                        placeholder="Ingresá la contraseña"
                        value={password}
                        onChange={(e) => {
                            setPassword(e.target.value);
                            setError(false);
                        }}
                        className={error ? 'error' : ''}
                        autoFocus
                    />

                    {error && (
                        <span className="error-text">Contraseña incorrecta</span>
                    )}

                    <button type="submit" className="btn btn-primary btn-large">
                        Entrar
                    </button>
                </form>

                <p className="password-footer">
                    Versión de prueba para usuarios seleccionados
                </p>
            </div>
        </div>
    );
}

export default PasswordGate;
