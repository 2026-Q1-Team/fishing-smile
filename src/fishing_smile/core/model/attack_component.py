from typing import (
    List,
    Literal,
)

from pydantic import (
    BaseModel,
    Field,
)

from .red_flag import RedFlag


class AttackComponent(BaseModel):
    kind: str
    name: str
    red_flags: List[RedFlag] = []


class EmailComponent(AttackComponent):
    kind: Literal['email']
    email_template: str


class HTMLComponent(AttackComponent):
    kind: Literal['html']
    url: str
    html_template: str


class APIComponent(AttackComponent):
    kind: Literal['api']
    url: str
