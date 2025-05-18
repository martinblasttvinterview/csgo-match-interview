import re
from abc import ABC, abstractmethod
from datetime import datetime

from pydantic import BaseModel


class BaseEvent(ABC, BaseModel):
    timestamp: datetime

    @classmethod
    @abstractmethod
    def get_regex_pattern(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_match(cls, match: re.Match) -> "BaseEvent":
        raise NotImplementedError


class BaseSchema(ABC, BaseModel):
    @classmethod
    @abstractmethod
    def get_regex_pattern(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_match(cls, match: re.Match, start_group: int) -> "BaseSchema":
        raise NotImplementedError
