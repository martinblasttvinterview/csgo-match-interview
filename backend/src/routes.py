from collections import defaultdict
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.events.enums import EventType
from src.events.event_interactor import GetEventInteractor
from src.schemas import (
    DataResponse,
    DatetimeInterval,
    KillsPerPlayerResponse,
    PlayerHeatmapResponse,
    PlayerKills,
    PlayerWithPosition,
    RoundAverageLengthResponse,
    RoundInterval,
    RoundNumericResponse,
    RoundWithNumeric,
)

if TYPE_CHECKING:
    from datetime import timedelta

router = APIRouter(prefix="/stats")


@router.get("/avg-round-time")
def get_average_round_length(
    interactor: GetEventInteractor,
) -> DataResponse[RoundAverageLengthResponse]:
    round_start_events = interactor.get_events(
        event_type=EventType.ROUND_START,
    )
    round_end_events = interactor.get_events(
        event_type=EventType.ROUND_END,
    )

    if len(round_start_events) != len(round_end_events):
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error.",
        )

    dt_list: list[timedelta] = [
        end.timestamp - start.timestamp
        for start, end in zip(
            round_start_events,
            round_end_events,
            strict=True,
        )
    ]

    return DataResponse(
        data=RoundAverageLengthResponse(
            average_seconds=(
                sum([dt.seconds for dt in dt_list]) // len(round_start_events)
            )
        )
    )


@router.get("/num-kills-players")
def get_kills_per_player(
    interactor: GetEventInteractor,
) -> DataResponse[KillsPerPlayerResponse]:
    player_kill_events = interactor.get_events(
        event_type=EventType.PLAYER_KILLED_PLAYER,
    )
    kills_count_map = defaultdict(int)

    for event in player_kill_events:
        kills_count_map[event.attacker.name] += 1

    kills = sorted(
        (
            PlayerKills(player_name=name, kills=count)
            for name, count in kills_count_map.items()
        ),
        key=lambda pk: pk.kills,
        reverse=True,
    )

    return DataResponse(data=KillsPerPlayerResponse(kills=kills))


@router.get("/player-kill-heatmap")
def get_player_kill_heatmap(
    interactor: GetEventInteractor,
    interval: Annotated[DatetimeInterval, Depends()],
) -> DataResponse[PlayerHeatmapResponse]:
    """Return coordinate data of players at the time of death."""
    player_kill_events = interactor.get_events(
        event_type=EventType.PLAYER_KILLED_PLAYER,
        interval=interval,
    )

    player_with_positions = [
        PlayerWithPosition(
            player_name=event.victim.name,
            x=event.victim_position.x,
            y=event.victim_position.y,
            weapon=event.weapon,
            timestamp=event.timestamp,
        )
        for event in player_kill_events
    ]

    return DataResponse(
        data=PlayerHeatmapResponse(player_with_positions=player_with_positions)
    )


@router.get("/money-spent-per-round")
def get_money_spent_per_round(
    interactor: GetEventInteractor,
    interval: Annotated[RoundInterval, Depends()],
) -> DataResponse[RoundNumericResponse]:
    round_to_purchase_map = interactor.get_events_per_rounds(
        event_type=EventType.PLAYER_PURCHASE,
        interval=interval,
    )
    round_to_total_map = {
        round_num: sum(event.money_spent for event in events)
        for round_num, events in round_to_purchase_map.items()
    }

    round_with_numerics = [
        RoundWithNumeric(
            round_num=round_num,
            numeric=numeric,
        )
        for round_num, numeric in round_to_total_map.items()
    ]

    return DataResponse(
        data=RoundNumericResponse(round_with_numeric=round_with_numerics)
    )
