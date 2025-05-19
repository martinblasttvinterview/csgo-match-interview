import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { PlayerKills } from '../types/chartTypes';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

interface KillsBarChartProps {
    data: PlayerKills[];
}

const KillsBarChart: React.FC<KillsBarChartProps> = ({ data }) => {
    if (!data || data.length === 0) return <div>No data available</div>;

    return (
        <ResponsiveContainer width="100%" height="90%">
            <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="player_name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="kills" fill="#8884d8">
                    {data.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Bar>
            </BarChart>
        </ResponsiveContainer>
    );
};

export default KillsBarChart;