from pydantic import (
    BaseModel,
    Field,
)

class TargetProfile(BaseModel):
    id: int | None = None
    name: str
    email: str
    phone_number: str | None = None
    company: str | None = None
    job_title: str | None = None

    @staticmethod
    def lookup(id: int):
        # TODO: lookup from database
        raise NotImplementedError
