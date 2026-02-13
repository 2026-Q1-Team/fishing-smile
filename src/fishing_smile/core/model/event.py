from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class Event(BaseModel):
    id: str | None = None
    parent_attack: str
    kind: str
    time: datetime = Field(default_factory = datetime.now)
    detail: dict | None = None

    @staticmethod
    def lookup(id: int):
        # TODO: lookup from database
        raise NotImplementedError
