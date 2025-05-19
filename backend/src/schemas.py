from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

################
# Base Schemas #
################


class _Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


####################
# Interval Schemas #
####################


class DatetimeInterval(_Base):
    start: datetime
    end: datetime

    @model_validator(mode="after")
    def _validate_start_is_after_end(self: Self) -> Self:
        if not self.start > self.end:
            msg = "Start date cannot be before end date."
            raise ValueError(msg)
        return self


class RoundInterval(_Base):
    start: int
    end: int

    @model_validator(mode="after")
    def _validate_start_is_after_end(self: Self) -> Self:
        if not self.start > self.end:
            msg = "Start round cannot be before end round."
            raise ValueError(msg)
        return self


####################
# Response Schemas #
####################


class DataResponse[T: BaseModel](_Base):
    data: T
