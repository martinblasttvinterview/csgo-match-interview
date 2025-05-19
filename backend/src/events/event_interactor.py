from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends

from src.events import BaseEvent, EventType
from src.parser import EventParser, get_event_parser
from src.schemas import DatetimeInterval


class EventInteractor:
    def __init__(
        self,
        event_parser: EventParser,
        logs_path: Path,
    ):
        self._parsed_events = event_parser.parse_file(logs_path)

    def _apply_interval(
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
        filtered = []
        for event in events:
            for k, v in filter_params.items():
                if not hasattr(event, k):
                    continue
                if getattr(event, k) != v:
                    continue
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

        events = self._parsed_events[event_type]

        if interval is not None:
            events = self._apply_interval(events, interval)

        if filter_params is not None:
            events = self._apply_filters(events, filter_params)

        return events


def get_event_interactor() -> EventInteractor:
    return EventInteractor(
        event_parser=get_event_parser(),
        logs_path=Path(__file__).parent.parent / "match-data.txt",
    )


GetInteractor = Annotated[EventInteractor, Depends(get_event_interactor)]
