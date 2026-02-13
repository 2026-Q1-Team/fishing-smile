from pydantic import (
    BaseModel,
    Field,
)


class RedFlag(BaseModel):
    kind: str
    name: str
    explanation: str
