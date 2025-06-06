from enum import StrEnum, auto


class EventType(StrEnum):
    PLAYER_ATTACK_PLAYER = auto()
    PLAYER_KILLED_PLAYER = auto()
    PLAYER_PURCHASE = auto()
    ROUND_START = auto()
    ROUND_END = auto()
    MATCH_STATUS_SCORE = auto()
