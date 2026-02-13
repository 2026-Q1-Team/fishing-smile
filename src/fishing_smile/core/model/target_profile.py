from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
)

class TargetProfile(BaseModel):
    id: Optional[str] = Field(None, alias = "UniqueID")
    name: str
    email: EmailStr
    phone_number: str | None = None
    company: str | None = None
    job_title: str | None = None

    @staticmethod
    def lookup(id: int):
        # TODO: lookup from database
        raise NotImplementedError
