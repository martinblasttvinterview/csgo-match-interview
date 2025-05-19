export interface PlayerKills {
    player_name: string;
    kills: number;
}

export interface PlayerWithPosition {
    x: number;
    y: number;
    weapon: string;
    timestamp?: string;
    player_name?: string;
}

export interface RoundWithNumeric {
    round_num: number;
    numeric: number;
}

export interface KillsPerPlayerResponse {
    kills: PlayerKills[];
}

export interface PlayerHeatmapResponse {
    player_with_positions: PlayerWithPosition[];
}

export interface RoundNumericResponse {
    round_with_numeric: RoundWithNumeric[];
}

export interface RoundAverageLengthResponse {
    average_seconds: number;
}