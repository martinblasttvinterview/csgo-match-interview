import re
from typing import ClassVar, Literal

from .bases import BaseSchema


class Player(BaseSchema):
    name: str
    user_id: int
    steam_id: str
    team: Literal["CT", "TERRORIST"] | None = None

    _pattern: ClassVar[str] = r'"(.+?)<(\d+)><(.+?)><(CT|TERRORIST)>"'

    @classmethod
    def get_regex_pattern(cls) -> str:
        return cls._pattern

    @classmethod
    def from_match(cls, match: re.Match, start_group: int) -> "Player":
        return cls(
            name=match.group(start_group),
            user_id=int(match.group(start_group + 1)),
            steam_id=match.group(start_group + 2),
            team=match.group(start_group + 3),
        )


class Position3D(BaseSchema):
    x: int
    y: int
    z: int  # likely not useful

    _pattern: ClassVar[str] = r"\[(-?\d+) (-?\d+) (-?\d+)\]"

    @classmethod
    def get_regex_pattern(cls) -> str:
        return cls._pattern

    @classmethod
    def from_match(cls, match: re.Match, start_group: int) -> "Position3D":
        return cls(
            x=int(match.group(start_group)),
            y=int(match.group(start_group + 1)),
            z=int(match.group(start_group + 2)),
        )
