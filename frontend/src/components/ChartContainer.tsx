import React, { ReactNode } from 'react';

interface ChartContainerProps {
    title: string;
    children: ReactNode;
}

const ChartContainer: React.FC<ChartContainerProps> = ({ title, children }) => {
    return (
        <div className="chart-container">
            <h3 className="chart-title">{title}</h3>
            {children}
        </div>
    );
};

export default ChartContainer;