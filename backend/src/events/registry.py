from typing import Any, ClassVar

from .bases import BaseEvent
from .enums import EventType


class EventRegistry:
    _events: ClassVar[dict[EventType, type[BaseEvent]]] = {}

    @classmethod
    def register(cls, event_type: EventType) -> Any:
        def decorator(event_cls: type[BaseEvent]) -> type[BaseEvent]:
            cls._events[event_type] = event_cls
            return event_cls

        return decorator

    @classmethod
    def get_events(cls) -> dict[EventType, type[BaseEvent]]:
        return cls._events.copy()
