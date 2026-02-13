from pydantic import (
    BaseModel,
    Field,
    EmailStr,
)

class TargetProfile(BaseModel):
    id: str | None = None
    name: str
    email: EmailStr
    phone: str | None = None
    company: str | None = None
    job_title: str | None = None

    @staticmethod
    def lookup(id: int):
        # TODO: lookup from database
        raise NotImplementedError
