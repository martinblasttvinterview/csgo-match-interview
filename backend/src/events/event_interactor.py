import itertools
from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends

from src.events import BaseEvent, EventType
from src.parser import EventParser, get_event_parser
from src.schemas import DatetimeInterval, RoundInterval


class EventInteractor:
    def __init__(
        self,
        event_parser: EventParser,
        logs_path: Path,
    ):
        self._parsed_events = event_parser.parse_file(logs_path)

    def _apply_datetime_interval(
        self, events: list[BaseEvent], interval: DatetimeInterval
    ) -> list[BaseEvent]:
        return [
            event
            for event in events
            if interval.start <= event.timestamp <= interval.end
        ]

    def _apply_filters(
        self, events: list[BaseEvent], filter_params: dict[str, Any]
    ) -> list[BaseEvent]:
        if not filter_params:
            return events

        def get_nested_attr(obj: Any, attr_path: str) -> Any:
            for attr in attr_path.split("."):
                if not hasattr(obj, attr):
                    return None
                obj = getattr(obj, attr)
            return obj

        filtered = []
        for event in events:
            match = True
            for key, expected_value in filter_params.items():
                actual_value = get_nested_attr(event, key)
                if actual_value != expected_value:
                    match = False
                    break
            if match:
                filtered.append(event)

        return filtered

    def get_events(
        self,
        event_type: EventType,
        interval: DatetimeInterval | None = None,
        filter_params: dict[str, Any] | None = None,
    ) -> list[BaseEvent]:
        if event_type not in self._parsed_events:
            return []

        print(event_type)

        events = self._parsed_events.get(event_type, [])

        if interval is not None:
            events = self._apply_datetime_interval(events, interval)

        if filter_params is not None:
            events = self._apply_filters(events, filter_params)

        return events

    def get_events_per_rounds(
        self,
        event_type: EventType,
        interval: RoundInterval | None = None,
        filter_params: dict[str, Any] | None = None,
    ) -> dict[int, list[BaseEvent]]:
        """
        Returns a mapping of round number to all events, of the specified event type,
        that happened for each round.
        """
        # Get all MATCH_STATUS_SCORE events, and skip every second one.
        # Skip, because each of those events has 2 entries per round.
        round_end_events = self.get_events(event_type=EventType.MATCH_STATUS_SCORE)
        round_end_events = round_end_events[::2]

        if not round_end_events:
            return {}

        first_timestamp = min(
            event.timestamp
            for events in self._parsed_events.values()
            for event in events
        )
        round_end_events = round_end_events[1:]

        datetime_intervals: list[DatetimeInterval] = []
        datetime_intervals.append(
            DatetimeInterval(start=first_timestamp, end=round_end_events[0].timestamp)
        )

        for prev, curr in itertools.pairwise(round_end_events):
            datetime_intervals.append(
                DatetimeInterval(start=prev.timestamp, end=curr.timestamp)
            )

        extra = 1
        if interval is not None:
            datetime_intervals = datetime_intervals[interval.start - 1 : interval.end]
            extra = interval.start

        events_per_round: dict[int, list[BaseEvent]] = {}
        for idx, dt_interval in enumerate(datetime_intervals, start=1):
            filtered_events = self.get_events(event_type, dt_interval, filter_params)
            events_per_round[idx + extra - 1] = filtered_events

        return events_per_round


def get_event_interactor() -> EventInteractor:
    return EventInteractor(
        event_parser=get_event_parser(),
        logs_path=Path(__file__).parent.parent.parent / "match-data.txt",
    )


GetEventInteractor = Annotated[EventInteractor, Depends(get_event_interactor)]
