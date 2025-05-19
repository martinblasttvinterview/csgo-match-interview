import axios from 'axios';

const API_BASE_URL = "http://localhost:8000/api/stats";

export const fetchAverageRoundTime = async () => {
    const response = await axios.get(`${API_BASE_URL}/avg-round-time`);
    return response.data.data;
};

export const fetchKillsPerPlayer = async () => {
    const response = await axios.get(`${API_BASE_URL}/num-kills-players`);
    return response.data.data;
};

export const fetchPlayerKillHeatmap = async (interval: { start: string; end: string }) => {
    const response = await axios.get(`${API_BASE_URL}/player-kill-heatmap`, {
        params: interval
    });
    return response.data.data;
};

export const fetchMoneySpentPerRound = async (interval: { start: number; end: number }) => {
    const response = await axios.get(`${API_BASE_URL}/money-spent-per-round`, {
        params: interval
    });
    return response.data.data;
};