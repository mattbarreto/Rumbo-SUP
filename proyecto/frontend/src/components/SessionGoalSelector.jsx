import { EnjoymentIcon, EffortIcon, WaveIcon } from './Icons';
import './SessionGoalSelector.css';

function SessionGoalSelector({ value, onChange }) {
    const goals = [
        {
            id: 'calma',
            icon: <EnjoymentIcon size={24} />,
            label: 'Calma',
            description: 'Relajación'
        },
        {
            id: 'entrenamiento',
            icon: <EffortIcon size={24} />,
            label: 'Entreno',
            description: 'Técnica'
        },
        {
            id: 'desafio',
            icon: <WaveIcon size={24} />,
            label: 'Desafío',
            description: 'Exigencia'
        }
    ];

    return (
        <div className="session-goal-selector">
            <div className="goal-segmented-control">
                {goals.map(goal => (
                    <button
                        key={goal.id}
                        className={`goal-segment ${value === goal.id ? 'active' : ''}`}
                        onClick={() => onChange(goal.id)}
                    >
                        <span className="goal-icon">{goal.icon}</span>
                        <span className="goal-label">{goal.label}</span>
                    </button>
                ))}
            </div>
            <div className="goal-description">
                {goals.find(g => g.id === value)?.description}
            </div>
        </div>
    );
}

export default SessionGoalSelector;
