import React, { useEffect, useState } from 'react';
import {
    fetchAverageRoundTime,
    fetchKillsPerPlayer,
    fetchPlayerKillHeatmap,
    fetchMoneySpentPerRound,
} from '../api/statsApi';
import type {
    PlayerKills,
    PlayerWithPosition,
    RoundWithNumeric,
} from '../types/chartTypes';
import KillsBarChart from './KillsBarChart';
import MoneyLineChart from './MoneyLineChart';
import KillHeatmapChart from './KillHeatmapChart';
import RoundTimeDisplay from './RoundTimeDisplay';
import WeaponKillsBarChart from './WeaponKillsBarChart';
import ChartContainer from './ChartContainer';

const ChartsGrid: React.FC = () => {
    const [killsData, setKillsData] = useState<PlayerKills[]>([]);
    const [heatmapData, setHeatmapData] = useState<PlayerWithPosition[]>([]);
    const [moneyData, setMoneyData] = useState<RoundWithNumeric[]>([]);
    const [avgRoundTime, setAvgRoundTime] = useState<number>(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [killsResp, heatmapResp, moneyResp, avgTimeResp] = await Promise.all([
                    fetchKillsPerPlayer(),
                    fetchPlayerKillHeatmap({ start: '2021-11-28T20:41:09Z', end: '2021-11-28T21:31:49Z' }),
                    fetchMoneySpentPerRound({ start: 1, end: 22 }),
                    fetchAverageRoundTime()
                ]);

                setKillsData(killsResp.kills);
                setHeatmapData(heatmapResp.player_with_positions);
                setMoneyData(moneyResp.round_with_numeric);
                setAvgRoundTime(avgTimeResp.average_seconds);
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch data');
                setLoading(false);
                console.error('Error fetching data:', err);
            }
        };

        fetchData();
    }, []);

    if (loading) return <div>Loading charts...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="charts-grid">
            <style jsx>{`
                .charts-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    grid-gap: 20px;
                    padding: 50px;
                }
            `}</style>

            <ChartContainer title="Money Spent per Round">
                <MoneyLineChart data={moneyData} />
            </ChartContainer>

            <ChartContainer title="Kills per Player">
                <KillsBarChart data={killsData} />
            </ChartContainer>

            <ChartContainer title="Weapon Kill Analysis">
                <WeaponKillsBarChart />
            </ChartContainer>

            <ChartContainer title="Player Death Heatmap">
                <KillHeatmapChart data={heatmapData} />
            </ChartContainer>

            <ChartContainer title="Average Round Time">
                <RoundTimeDisplay averageSeconds={avgRoundTime} />
            </ChartContainer>
        </div>
    );
};

export default ChartsGrid;