import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import OnboardingFlow from './components/OnboardingFlow';
import MainScreen from './components/MainScreen';
import SenseiScreen from './components/SenseiScreen';
import ProfileScreen from './components/ProfileScreen';
import AboutScreen from './components/AboutScreen';
import PasswordGate from './components/PasswordGate';
import { isMobile, isDevMode } from './utils/deviceDetection';

function App() {
    const [isMobileDevice, setIsMobileDevice] = useState(true);
    const [hasCompletedOnboarding, setHasCompletedOnboarding] = useState(false);

    useEffect(() => {
        // Detección de dispositivo móvil (o modo desarrollo)
        const isValidDevice = isMobile() || isDevMode();
        setIsMobileDevice(isValidDevice);

        // Verificar si completó onboarding
        const profile = localStorage.getItem('userProfile');
        setHasCompletedOnboarding(!!profile);
    }, []);

    // Bloqueo para desktop
    if (!isMobileDevice) {
        return (
            <div className="desktop-block active">
                <div>
                    <h1>📱 Solo Móviles</h1>
                    <p>Rumbo SUP está diseñado para dispositivos móviles.</p>
                    <p>Por favor, accede desde tu teléfono o tablet.</p>
                </div>
            </div>
        );
    }

    return (
        <PasswordGate>
            <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
                <Routes>
                    {!hasCompletedOnboarding ? (
                        <>
                            <Route path="/onboarding" element={<OnboardingFlow onComplete={() => setHasCompletedOnboarding(true)} />} />
                            <Route path="*" element={<Navigate to="/onboarding" replace />} />
                        </>
                    ) : (
                        <>
                            <Route path="/" element={<MainScreen />} />
                            <Route path="/sensei" element={<SenseiScreen />} />
                            <Route path="/profile" element={<ProfileScreen />} />
                            <Route path="/about" element={<AboutScreen />} />
                            <Route path="*" element={<Navigate to="/" replace />} />
                        </>
                    )}
                </Routes>
            </BrowserRouter>
        </PasswordGate>
    );
}

export default App;

