import axios from 'axios';
import type {
    DataResponse,
    RoundNumericResponse,
    StringListResponse,
    KillsPerPlayerResponse,
    PlayerHeatmapResponse,
    RoundAverageLengthResponse,
    RoundWithNumeric,
} from '../types/chartTypes';

const API_BASE_URL = "http://localhost:8000/api/stats";

const apiGet = async <T>(url: string, params?: any): Promise<T> => {
    try {
        const response = await axios.get<DataResponse<T>>(url, { params });
        return response.data.data;
    } catch (error) {
        console.error(`API Error at ${url}:`, error);
        throw error;
    }
};

export const fetchAverageRoundTime = async (): Promise<RoundAverageLengthResponse> => {
    return apiGet<RoundAverageLengthResponse>(`${API_BASE_URL}/avg-round-time`);
};

export const fetchKillsPerPlayer = async (): Promise<KillsPerPlayerResponse> => {
    return apiGet<KillsPerPlayerResponse>(`${API_BASE_URL}/num-kills-players`);
};

export const fetchPlayerKillHeatmap = async (
    interval: { start: string; end: string }
): Promise<PlayerHeatmapResponse> => {
    return apiGet<PlayerHeatmapResponse>(`${API_BASE_URL}/player-kill-heatmap`, interval);
};

export const fetchMoneySpentPerRound = async (
    interval: { start: number; end: number }
): Promise<RoundNumericResponse> => {
    return apiGet<RoundNumericResponse>(`${API_BASE_URL}/money-spent-per-round`, interval);
};

export const fetchWeaponKills = async (
    weapon: string,
    startRound: number,
    endRound: number
): Promise<RoundWithNumeric[]> => {
    const response = await apiGet<RoundNumericResponse>(
        `${API_BASE_URL}/kills-by-weapon/${weapon}`,
        { start_round: startRound, end_round: endRound }
    );
    return response.round_with_numeric;
};

export const fetchAllWeapons = async (): Promise<string[]> => {
    const response = await apiGet<StringListResponse>(`${API_BASE_URL}/weapons`);
    return response.strings;
};