// src/components/charts/KillHeatmapChart.tsx
import React, { useState, useEffect } from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { PlayerWithPosition } from '../types/chartTypes';
import { Box, Slider, Typography } from '@mui/material';
import { DateTime } from 'luxon';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

interface KillHeatmapChartProps {
    data: PlayerWithPosition[];
}

const KillHeatmapChart: React.FC<KillHeatmapChartProps> = ({ data }) => {
    const [filteredData, setFilteredData] = useState<PlayerWithPosition[]>([]);
    const [dateRange, setDateRange] = useState<[number, number]>([0, 0]);
    const [timestamps, setTimestamps] = useState<number[]>([]);

    useEffect(() => {
        if (data && data.length > 0) {
            const sortedTimestamps = data
                .map(item => new Date(item.timestamp).getTime())
                .sort((a, b) => a - b);

            setTimestamps(sortedTimestamps);

            setDateRange([sortedTimestamps[0], sortedTimestamps[sortedTimestamps.length - 1]]);
            setFilteredData(data);
        }
    }, [data]);

    const handleDateChange = (_: Event, newValue: number | number[]) => {
        const newRange = newValue as [number, number];
        setDateRange(newRange);

        const filtered = data.filter(item => {
            const itemTime = new Date(item.timestamp).getTime();
            return itemTime >= newRange[0] && itemTime <= newRange[1];
        });
        setFilteredData(filtered);
    };

    if (!data || data.length === 0) return <div>No data available</div>;

    const formatDate = (timestamp: number) => {
        return DateTime.fromMillis(timestamp).toFormat('yyyy-MM-dd HH:mm');
    };

    return (
        <div style={{ width: '100%', height: '100%' }}>
            <Box sx={{ width: '100%', padding: '0 20px', marginBottom: '10px' }}>
                <Typography gutterBottom>
                    Time Range: {formatDate(dateRange[0])} to {formatDate(dateRange[1])}
                </Typography>
                <Slider
                    value={dateRange}
                    onChange={handleDateChange}
                    min={timestamps[0] || 0}
                    max={timestamps[timestamps.length - 1] || 0}
                    step={(timestamps[timestamps.length - 1] - timestamps[0]) / 1000}
                    valueLabelDisplay="auto"
                    valueLabelFormat={formatDate}
                    marks={[
                        {
                            value: timestamps[0] || 0,
                            label: formatDate(timestamps[0] || 0)
                        },
                        {
                            value: timestamps[timestamps.length - 1] || 0,
                            label: formatDate(timestamps[timestamps.length - 1] || 0)
                        }
                    ]}
                />
            </Box>

            <ResponsiveContainer width="100%" height="80%">
                <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                    <CartesianGrid />
                    <XAxis type="number" dataKey="x" name="X Coordinate" />
                    <YAxis type="number" dataKey="y" name="Y Coordinate" />
                    <ZAxis dataKey="weapon" name="Weapon" />
                    <Tooltip
                        cursor={{ strokeDasharray: '3 3' }}
                        formatter={(value, name, _) => {
                            if (name === 'timestamp') {
                                return [formatDate(new Date(value).getTime()), name];
                            }
                            return [value, name];
                        }}
                    />
                    <Scatter name="Kills" data={filteredData} fill="#ff7300">
                        {filteredData.map((_, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                    </Scatter>
                </ScatterChart>
            </ResponsiveContainer>
        </div>
    );
};

export default KillHeatmapChart;