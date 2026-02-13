from pydantic import (
    BaseModel,
    Field,
)


class Attack(BaseModel):
    id: str | None = None
    external_id: str
    scheme: str  # AttackScheme
    target: str  # TargetProfile?

    @staticmethod
    def lookup(id: int):
        # TODO: lookup from database
        raise NotImplementedError
