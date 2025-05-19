import re
from pathlib import Path

from src.events import BaseEvent, EventType
from src.events.registry import EventRegistry
from src.settings import settings


class EventParser:
    def __init__(
        self,
        event_types: dict[EventType, type[BaseEvent]],
    ):
        self._event_types = event_types

    def parse_line(self, line: str) -> tuple[EventType, BaseEvent] | None:
        for event_type, event in self._event_types.items():
            pattern = event.get_regex_pattern()
            match = re.fullmatch(pattern, line.strip())
            if match:
                return event_type, event.from_match(match)
        return None

    def parse_file(
        self,
        file_path: Path,
        # logs outside of this range are pretty much useless
        start_line: int = 1863,
        end_line: int | None = 9146,
    ) -> dict[EventType, list[BaseEvent]]:
        event_groups: dict[EventType, list[BaseEvent]] = {
            event_type: [] for event_type in self._event_types
        }

        with file_path.open() as f:
            for current_line_number, line in enumerate(f):
                if settings.env != "test":
                    if current_line_number < start_line:
                        continue
                    if end_line is not None and current_line_number >= end_line:
                        break

                parsed = self.parse_line(line)
                if parsed:
                    event_name, event = parsed
                    event_groups[event_name].append(event)

        return {k: v for k, v in event_groups.items() if v}


def get_event_parser() -> EventParser:
    return EventParser(event_types=EventRegistry.get_events())
