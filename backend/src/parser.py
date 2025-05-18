import re
from pathlib import Path

from src.events.events import BaseEvent
from src.events import EventType


class EventParser:
    def __init__(
        self,
        event_types: dict[EventType, type[BaseEvent]],
    ):
        self.event_types = event_types

    def parse_line(self, line: str) -> tuple[EventType, BaseEvent] | None:
        for event_type, event in self.event_types.items():
            pattern = event.get_regex_pattern()
            match = re.fullmatch(pattern, line.strip())
            if match:
                return event_type, event.from_match(match)
        return None

    def parse_file(
        self,
        file_path: Path,
        skip_lines: int = 1863,  # lines before this are pretty much irrelevant
    ) -> dict[EventType, list[BaseEvent]]:
        event_groups: dict[EventType, list[BaseEvent]] = {
            event_type: [] for event_type in self.event_types
        }

        with file_path.open() as f:
            for _ in range(skip_lines):
                next(f, None)

            for line in f:
                parsed = self.parse_line(line)
                if parsed:
                    event_name, event = parsed
                    event_groups[event_name].append(event)

        return {k: v for k, v in event_groups.items() if v}
