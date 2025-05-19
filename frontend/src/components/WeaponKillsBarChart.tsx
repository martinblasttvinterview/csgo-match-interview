import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { fetchWeaponKills, fetchAllWeapons } from '../api/statsApi';
import { Box, Select, MenuItem, FormControl, InputLabel, Slider, Typography } from '@mui/material';

interface RoundKillData {
    round_num: number;
    kills: number;
}

const WeaponKillsBarChart: React.FC = () => {
    const [weapons, setWeapons] = useState<string[]>([]);
    const [selectedWeapon, setSelectedWeapon] = useState<string>('');
    const [allRoundKills, setAllRoundKills] = useState<RoundKillData[]>([]);
    const [filteredKills, setFilteredKills] = useState<RoundKillData[]>([]);
    const [roundRange, setRoundRange] = useState<[number, number]>([1, 22]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadWeapons = async () => {
            try {
                const weaponsList = await fetchAllWeapons();
                setWeapons(weaponsList);
                if (weaponsList.length > 0) {
                    setSelectedWeapon(weaponsList[0]);
                }
            } catch (error) {
                console.error('Error fetching weapons:', error);
            }
        };
        loadWeapons();
    }, []);

    useEffect(() => {
        const loadWeaponKills = async () => {
            if (!selectedWeapon) return;

            setLoading(true);
            try {
                const killsData = await fetchWeaponKills(selectedWeapon, 1, 22);

                const roundData = killsData.map(item => ({
                    round_num: item.round_num,
                    kills: item.numeric
                }))
                    .sort((a, b) => a.round_num - b.round_num);

                setAllRoundKills(roundData);
                setFilteredKills(roundData);
                setRoundRange([1, 22]);
            } catch (error) {
                console.error('Error fetching weapon kills:', error);
            } finally {
                setLoading(false);
            }
        };
        loadWeaponKills();
    }, [selectedWeapon]);

    useEffect(() => {
        if (allRoundKills.length > 0) {
            const filtered = allRoundKills.filter(
                item => item.round_num >= roundRange[0] && item.round_num <= roundRange[1]
            );
            setFilteredKills(filtered);
        }
    }, [roundRange, allRoundKills]);

    const handleWeaponChange = (event: any) => {
        setSelectedWeapon(event.target.value as string);
    };

    const handleRoundChange = (_: Event, newValue: number | number[]) => {
        setRoundRange(newValue as [number, number]);
    };

    if (loading && allRoundKills.length === 0) return <div>Loading weapon data...</div>;

    const maxKills = Math.max(...filteredKills.map(item => item.kills), 0);
    const yAxisDomain = [0, Math.ceil(maxKills)];

    return (
        <div style={{ width: '100%', height: '100%' }}>
            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                <FormControl fullWidth>
                    <InputLabel>Weapon</InputLabel>
                    <Select
                        value={selectedWeapon}
                        onChange={handleWeaponChange}
                        label="Weapon"
                    >
                        {weapons.map((weapon) => (
                            <MenuItem key={weapon} value={weapon}>
                                {weapon}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                <Box sx={{ width: 300 }}>
                    <Typography gutterBottom>
                        Round Range: {roundRange[0]} - {roundRange[1]}
                    </Typography>
                    <Slider
                        value={roundRange}
                        onChange={handleRoundChange}
                        valueLabelDisplay="auto"
                        min={1}
                        max={22}
                        step={1}
                        marks={[
                            { value: 1, label: '1' },
                            { value: 22, label: '22' }
                        ]}
                    />
                </Box>
            </Box>

            <Typography variant="subtitle1" gutterBottom sx={{ mb: 2 }}>
                {selectedWeapon} Kills (Rounds {roundRange[0]}-{roundRange[1]})
            </Typography>

            <ResponsiveContainer width="100%" height="80%">
                <BarChart
                    data={filteredKills}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                        dataKey="round_num"
                        label={{ value: 'Round Number', position: 'insideBottomRight', offset: -10 }}
                    />
                    <YAxis
                        domain={yAxisDomain}
                        tickCount={maxKills + 1}
                        allowDecimals={false}
                        label={{ value: 'Kills', angle: -90, position: 'insideLeft' }}
                    />
                    <Tooltip
                        formatter={(value) => [`${value} kills`, 'Kills']}
                        labelFormatter={(round) => `Round ${round}`}
                    />
                    <Legend />
                    <Bar
                        dataKey="kills"
                        name="Kills"
                        fill="#8884d8"
                        animationDuration={1000}
                    />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default WeaponKillsBarChart;