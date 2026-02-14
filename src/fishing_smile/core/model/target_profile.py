from sqlmodel import (
    Field,
    SQLModel,
)
from pydantic import (
    EmailStr,
)


class TargetProfile(SQLModel, table = True):
    id: int | None = Field(
        default = None,
        primary_key = True,
    )
    name: str = Field(
        index = True,
        max_length = 64,
    )
    email: EmailStr = Field(
        index = True,
        max_length = 64,
    )
    phone: str | None = Field(
        default = None,
        max_length = 16,
    )
    company: str | None = Field(
        default = None,
        max_length = 64,
    )
    job_title: str | None = Field(
        default = None,
        max_length = 64,
    )
