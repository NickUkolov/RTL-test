from datetime import datetime
from enum import Enum

from pydantic import BaseModel, model_validator


class GroupType(
    str,
    Enum,
):
    hour = "hour"
    day = "day"
    month = "month"


class AggregateIn(BaseModel):
    dt_from: datetime
    dt_upto: datetime
    group_type: GroupType

    @model_validator(mode="after")
    def verify_square(self):
        if self.dt_from > self.dt_upto:
            raise ValueError("Date from is more than upto date")
        return self
