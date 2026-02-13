from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class Attack(BaseModel):
    id: Optional[str] = Field(None, alias="UniqueID")
    unique_random_code: str
    scheme: str  # AttackScheme
    target: str  # TargetProfile?
