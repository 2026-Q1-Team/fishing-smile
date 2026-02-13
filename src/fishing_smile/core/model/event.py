from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class Event(BaseModel):
    id: Optional[str] = Field(None, alias = "UniqueID")
    part_of_which_attack: str
    kind: str
    timestamp: datetime = Field(default_factory = datetime.now)
    details: Optional[dict] = None
