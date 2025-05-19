import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import type { RoundWithNumeric } from '../types/chartTypes';
import { Box, Slider, Typography } from '@mui/material';

interface MoneyLineChartProps {
    data: RoundWithNumeric[];
}

const MoneyLineChart: React.FC<MoneyLineChartProps> = ({ data }) => {
    const [filteredData, setFilteredData] = useState<RoundWithNumeric[]>([]);
    const [roundRange, setRoundRange] = useState<[number, number]>([1, 1]);

    useEffect(() => {
        if (data && data.length > 0) {
            const minRound = Math.min(...data.map(item => item.round_num));
            const maxRound = Math.max(...data.map(item => item.round_num));
            setRoundRange([minRound, maxRound]);
            setFilteredData(data);
        }
    }, [data]);

    const handleRangeChange = (event: Event, newValue: number | number[]) => {
        const newRange = newValue as [number, number];
        setRoundRange(newRange);

        const filtered = data.filter(item =>
            item.round_num >= newRange[0] && item.round_num <= newRange[1]
        );
        setFilteredData(filtered);
    };

    if (!data || data.length === 0) return <div>No data available</div>;

    return (
        <div style={{ width: '100%', height: '100%' }}>
            <Box sx={{ width: '100%', padding: '0 20px', marginBottom: '10px' }}>
                <Typography gutterBottom>
                    Round Range: {roundRange[0]} - {roundRange[1]}
                </Typography>
                <Slider
                    value={roundRange}
                    onChange={handleRangeChange}
                    valueLabelDisplay="auto"
                    min={Math.min(...data.map(item => item.round_num))}
                    max={Math.max(...data.map(item => item.round_num))}
                    step={1}
                    marks={[
                        { value: Math.min(...data.map(item => item.round_num)), label: 'First' },
                        { value: Math.max(...data.map(item => item.round_num)), label: 'Last' }
                    ]}
                />
            </Box>

            <ResponsiveContainer width="100%" height="80%">
                <LineChart data={filteredData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="round_num" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="numeric" stroke="#82ca9d" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default MoneyLineChart;