import './MetricCard.css';

function MetricCard({ label, score, categoria, icon }) {
    // Determinar color según categoría
    const getColor = () => {
        if (categoria === 'alto') return 'var(--safe-green)';
        if (categoria === 'medio') return 'var(--caution-yellow)';
        return 'var(--danger-red)';
    };

    // Traducir categoría
    const getCategoriaText = () => {
        if (categoria === 'alto') return 'Alto';
        if (categoria === 'medio') return 'Medio';
        return 'Bajo';
    };

    return (
        <div className="metric-card">
            <div className="metric-header">
                {icon && <span className="metric-icon">{icon}</span>}
                <span className="metric-label">{label}</span>
            </div>

            <div className="metric-value">
                {score}
                <span className="metric-total">/100</span>
            </div>

            <div className="metric-category">
                <span className={`badge badge-${categoria}`}>
                    {getCategoriaText()}
                </span>
            </div>
        </div>
    );
}

export default MetricCard;
