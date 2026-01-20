import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { WaveIcon, GithubIcon, LinkedinIcon, GlobeIcon, CodeIcon } from './Icons';
import './AboutScreen.css';

function AboutScreen() {
    const navigate = useNavigate();

    return (
        <motion.div
            className="page about-screen"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{
                type: 'spring',
                stiffness: 300,
                damping: 30
            }}
        >
            <div className="container">
                <div className="about-header">
                    <button className="btn-back-nav" onClick={() => navigate('/profile')}>
                        ← Perfil
                    </button>
                    <h1>Acerca de Rumbo</h1>
                </div>

                <div className="about-card glass-card-premium">
                    <div className="app-meta">
                        <div className="app-logo">
                            <WaveIcon size={48} className="logo-icon" />
                            <h2>Rumbo SUP</h2>
                        </div>
                        <span className="version-badge">v1.0.0 (Oceanic)</span>
                        <p className="app-description">
                            Asistente digital para Stand Up Paddle, diseñado para amplificar tu conexión con el mar.
                        </p>
                    </div>
                </div>

                <div className="creator-card">
                    <div className="creator-header">
                        <h3>Creado por</h3>
                        <h2>Matías Barreto</h2>
                        <p className="creator-role">Creative Technologist & AI Designer</p>
                    </div>

                    <p className="creator-bio">
                        Diseñando infraestructuras tecnológicas y sistemas que amplifican la inteligencia colectiva.
                    </p>

                    <div className="social-links">
                        <a href="https://matiasbarreto.com/" target="_blank" rel="noopener noreferrer" className="social-link">
                            <GlobeIcon size={20} />
                            <span>Website</span>
                        </a>
                        <a href="https://www.linkedin.com/in/matiasbarreto/" target="_blank" rel="noopener noreferrer" className="social-link">
                            <LinkedinIcon size={20} />
                            <span>LinkedIn</span>
                        </a>
                        <a href="https://github.com/mattbarreto" target="_blank" rel="noopener noreferrer" className="social-link">
                            <GithubIcon size={20} />
                            <span>GitHub</span>
                        </a>
                    </div>
                </div>

                <div className="tech-card glass-card">
                    <div className="tech-header">
                        <CodeIcon size={24} className="tech-icon" />
                        <div>
                            <h3>Código Abierto</h3>
                            <p>Transparente y colaborativo.</p>
                        </div>
                    </div>
                    <a href="https://github.com/mattbarreto/rumbo-sup" target="_blank" rel="noopener noreferrer" className="btn btn-outline">
                        Ver Repositorio
                    </a>
                </div>

                <div className="footer-credits">
                    <p>Hecho con 💙 y 🌊 en Buenos Aires</p>
                </div>
            </div>
        </motion.div>
    );
}

export default AboutScreen;
