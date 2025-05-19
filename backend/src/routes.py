from typing import TYPE_CHECKING

from fastapi import APIRouter

from src.events.enums import EventType
from src.events.event_interactor import GetInteractor
from src.schemas import DataResponse, RoundAverageLengthResponse

if TYPE_CHECKING:
    from datetime import timedelta

router = APIRouter(prefix="/stats")


@router.get("/avg-round-time")
def get_average_round_length(
    interactor: GetInteractor,
) -> DataResponse[RoundAverageLengthResponse]:
    round_start_events = interactor.get_events(
        event_type=EventType.ROUND_START,
    )
    round_end_events = interactor.get_events(
        event_type=EventType.ROUND_END,
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
