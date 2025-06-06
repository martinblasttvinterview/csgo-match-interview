__all__ = [
    "BaseEvent",
    "BaseSchema",
    "EventRegistry",
    "EventType",
]

import re
from datetime import UTC, datetime
from typing import ClassVar

from .bases import BaseEvent, BaseSchema
from .enums import EventType
from .registry import EventRegistry
from .schemas import Player, Position3D


@EventRegistry.register(EventType.PLAYER_ATTACK_PLAYER)
class PlayerAttackPlayerEvent(BaseEvent):
    attacker: Player
    attacker_position: Position3D
    victim: Player
    victim_position: Position3D
    weapon: str
    damage: int
    damage_armor: int
    health: int
    armor: int
    hitgroup: str

    _pattern: ClassVar[str] = (
        r"^{timestamp}: "
        r"{player_pattern} "
        r"{position_pattern} attacked "
        r"{player_pattern} "
        r'{position_pattern} with "{weapon}" '
        r'\(damage "{damage}"\) \(damage_armor "{damage_armor}"\) '
        r'\(health "{health}"\) \(armor "{armor}"\) '
        r'\(hitgroup "{hitgroup}"\)$'
    ).format(
        timestamp=r"(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})",
        player_pattern=Player.get_regex_pattern(),
        position_pattern=Position3D.get_regex_pattern(),
        weapon=r"(.+?)",
        damage=r"(\d+)",
        damage_armor=r"(\d+)",
        health=r"(\d+)",
        armor=r"(\d+)",
        hitgroup=r"(.+?)",
    )

    @classmethod
    def get_regex_pattern(cls) -> str:
        return cls._pattern

    @classmethod
    def from_match(
        cls,
        match: re.Match,
    ) -> "PlayerAttackPlayerEvent":
        timestamp = datetime.strptime(match.group(1), "%m/%d/%Y - %H:%M:%S").replace(
            tzinfo=UTC
        )
        attacker = Player.from_match(match, start_group=2)
        attacker_pos = Position3D.from_match(match, start_group=6)
        victim = Player.from_match(match, start_group=9)
        victim_pos = Position3D.from_match(match, start_group=13)

        return cls(
            timestamp=timestamp,
            attacker=attacker,
            attacker_position=attacker_pos,
            victim=victim,
            victim_position=victim_pos,
            weapon=match.group(16),
            damage=int(match.group(17)),
            damage_armor=int(match.group(18)),
            health=int(match.group(19)),
            armor=int(match.group(20)),
            hitgroup=match.group(21),
        )


@EventRegistry.register(EventType.PLAYER_KILLED_PLAYER)
class PlayerKilledPlayerEvent(BaseEvent):
    attacker: Player
    attacker_position: Position3D
    victim: Player
    victim_position: Position3D
    weapon: str

    _pattern: ClassVar[str] = (
        r"^{timestamp}: "
        r"{attacker} "
        r"{attacker_pos} killed "
        r"{victim} "
        r"{victim_pos} with \"{weapon}\"$"
    ).format(
        timestamp=r"(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})",
        attacker=Player.get_regex_pattern(),
        attacker_pos=Position3D.get_regex_pattern(),
        victim=Player.get_regex_pattern(),
        victim_pos=Position3D.get_regex_pattern(),
        weapon=r"(.+?)",
    )

    @classmethod
    def get_regex_pattern(cls) -> str:
        return cls._pattern

    @classmethod
    def from_match(cls, match: re.Match) -> "PlayerKilledPlayerEvent":
        timestamp = datetime.strptime(match.group(1), "%m/%d/%Y - %H:%M:%S").replace(
            tzinfo=UTC
        )
        attacker = Player.from_match(match, start_group=2)
        attacker_pos = Position3D.from_match(match, start_group=6)
        victim = Player.from_match(match, start_group=9)
        victim_pos = Position3D.from_match(match, start_group=13)
        weapon = match.group(16)

        return cls(
            timestamp=timestamp,
            attacker=attacker,
            attacker_position=attacker_pos,
            victim=victim,
            victim_position=victim_pos,
            weapon=weapon,
        )


@EventRegistry.register(EventType.PLAYER_PURCHASE)
class PlayerPurchaseEvent(BaseEvent):
    player: Player
    item: str
    money_before: int
    money_after: int
    money_spent: int

    _pattern: ClassVar[str] = (
        r"^{timestamp}: "
        r"{player_pattern} "
        r"money change {money_before}-{money_spent} = \${money_after} "
        r"\(tracked\) \(purchase: {item}\)$"
    ).format(
        timestamp=r"(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})",
        player_pattern=Player.get_regex_pattern(),
        money_before=r"(\d+)",
        money_spent=r"(\d+)",
        money_after=r"(\d+)",
        item=r"(.+?)",
    )

    @classmethod
    def get_regex_pattern(cls) -> str:
        return cls._pattern

    @classmethod
    def from_match(cls, match: re.Match) -> "PlayerPurchaseEvent":
        timestamp = datetime.strptime(match.group(1), "%m/%d/%Y - %H:%M:%S").replace(
            tzinfo=UTC
        )
        player = Player.from_match(match, start_group=2)

        return cls(
            timestamp=timestamp,
            player=player,
            money_before=int(match.group(6)),
            money_spent=int(match.group(7)),
            money_after=int(match.group(8)),
            item=match.group(9),
        )


@EventRegistry.register(EventType.ROUND_START)
class RoundStartEvent(BaseEvent):
    _pattern: ClassVar[str] = (r'^{timestamp}: World triggered "Round_Start"$').format(
        timestamp=r"(?P<timestamp>\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})"
    )

    @classmethod
    def get_regex_pattern(cls) -> str:
        return cls._pattern

    @classmethod
    def from_match(cls, match: re.Match) -> "RoundStartEvent":
        timestamp = datetime.strptime(
            match.group("timestamp"), "%m/%d/%Y - %H:%M:%S"
        ).replace(tzinfo=UTC)
        return cls(timestamp=timestamp)


@EventRegistry.register(EventType.ROUND_END)
class RoundEndEvent(BaseEvent):
    _pattern: ClassVar[str] = (r'^{timestamp}: World triggered "Round_End"$').format(
        timestamp=r"(?P<timestamp>\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})"
    )

    @classmethod
    def get_regex_pattern(cls) -> str:
        return cls._pattern

    @classmethod
    def from_match(cls, match: re.Match) -> "RoundEndEvent":
        timestamp = datetime.strptime(
            match.group("timestamp"), "%m/%d/%Y - %H:%M:%S"
        ).replace(tzinfo=UTC)
        return cls(timestamp=timestamp)


@EventRegistry.register(EventType.MATCH_STATUS_SCORE)
class MatchStatusScoreEvent(BaseEvent):
    score_team1: int
    score_team2: int
    map_name: str
    rounds_played: int

    _pattern: ClassVar[str] = (
        r'^{timestamp}: MatchStatus: Score: {score_team1}:{score_team2} on map "{map_name}" RoundsPlayed: {rounds_played}$'
    ).format(
        timestamp=r"(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})",
        score_team1=r"(\d+)",
        score_team2=r"(\d+)",
        map_name=r"(.+?)",
        rounds_played=r"(\d+)",
    )

    @classmethod
    def get_regex_pattern(cls) -> str:
        return cls._pattern

    @classmethod
    def from_match(cls, match: re.Match) -> "MatchStatusScoreEvent":
        timestamp = datetime.strptime(match.group(1), "%m/%d/%Y - %H:%M:%S").replace(
            tzinfo=UTC
        )
        return cls(
            timestamp=timestamp,
            score_team1=int(match.group(2)),
            score_team2=int(match.group(3)),
            map_name=match.group(4),
            rounds_played=int(match.group(5)),
        )
