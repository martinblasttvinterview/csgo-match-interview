from datetime import UTC, datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

################
# Base Schemas #
################


class _Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


####################
# Interval Schemas #
####################


class DatetimeInterval(_Base):
    start: datetime = Field(default=datetime(2021, 11, 28, 20, 41, 9, tzinfo=UTC))
    end: datetime = Field(default=datetime(2021, 11, 28, 21, 31, 49, tzinfo=UTC))

    @model_validator(mode="after")
    def _validate_start_is_after_end(self: Self) -> Self:
        if not self.start <= self.end:
            msg = "Start date cannot be before end date."
            raise ValueError(msg)
        return self


class RoundInterval(_Base):
    start: int = Field(default=1)
    end: int = Field(default=22)

    @model_validator(mode="after")
    def _validate_start_is_after_end(self: Self) -> Self:
        if not self.start <= self.end:
            msg = "Start round cannot be before end round."
            raise ValueError(msg)
        return self


####################
# Response Schemas #
####################


class DataResponse[T: BaseModel](_Base):
    data: T


class RoundAverageLengthResponse(_Base):
    average_seconds: int = Field(
        ..., description="Average length of the rounds in seconds"
    )


class PlayerKills(_Base):
    player_name: str = Field(..., description="Name of the player")
    kills: int = Field(..., description="Total kills made by the player")


class KillsPerPlayerResponse(_Base):
    kills: list[PlayerKills] = Field(
        ..., description="List of players and their respective kill counts"
    )


class PlayerWithPosition(_Base):
    player_name: str = Field(..., description="Name of the player")
    x: int
    y: int
    weapon: str
    timestamp: datetime


class PlayerHeatmapResponse(_Base):
    player_with_positions: list[PlayerWithPosition] = Field(
        ..., description="List of players and their position"
    )


class RoundWithNumeric(_Base):
    round_num: int
    numeric: int | float


class RoundNumericResponse(_Base):
    round_with_numeric: list[RoundWithNumeric] = Field(
        ..., description="List of rounds with numeric data for each."
    )


class StringListResponse(_Base):
    strings: list[str]
