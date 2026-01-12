import { motion } from 'framer-motion';
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
                    <motion.button
                        key={goal.id}
                        className={`goal-segment ${value === goal.id ? 'active' : ''}`}
                        onClick={() => onChange(goal.id)}
                        whileHover={{
                            scale: 1.05,
                            transition: { type: 'spring', stiffness: 400, damping: 17 }
                        }}
                        whileTap={{
                            scale: 0.95,
                            transition: { type: 'spring', stiffness: 400, damping: 17 }
                        }}
                        animate={value === goal.id ? {
                            scale: [1, 1.08, 1],
                            transition: { type: 'spring', stiffness: 300, damping: 20 }
                        } : {}}
                    >
                        <span className="goal-icon">{goal.icon}</span>
                        <span className="goal-label">{goal.label}</span>
                    </motion.button>
                ))}
            </div>
            <motion.div
                className="goal-description"
                key={value}
                initial={{ opacity: 0, y: -5 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ type: 'spring', stiffness: 300, damping: 25 }}
            >
                {goals.find(g => g.id === value)?.description}
            </motion.div>
        </div>
    );
}

export default SessionGoalSelector;
