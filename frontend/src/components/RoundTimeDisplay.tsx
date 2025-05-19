// src/components/charts/RoundTimeDisplay.tsx
import React from 'react';

interface RoundTimeDisplayProps {
    averageSeconds: number;
}

const RoundTimeDisplay: React.FC<RoundTimeDisplayProps> = ({ averageSeconds }) => {
    return (
        <div style={{
            height: '90%',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            fontSize: '2rem',
            fontWeight: 'bold'
        }}>
            {Math.floor(averageSeconds / 60)}m {averageSeconds % 60}s
        </div>
    );
};

export default RoundTimeDisplay;