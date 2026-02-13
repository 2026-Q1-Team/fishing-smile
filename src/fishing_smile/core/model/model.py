from typing import (
    List,
    Optional,
    Union,
)
from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
)


class RedFlag(BaseModel):
    kind: str
    name: str
    explanation: str


class AttackComponent(BaseModel):
    kind: str
    name: str
    red_flags: List[RedFlag] = []


class EmailComponent(AttackComponent):
    email_template: str


class HTMLComponent(AttackComponent):
    url: str
    html_template: str


class APIComponent(AttackComponent):
    url: str


class AttackScheme(BaseModel):
    name: str
    components: List[Union[EmailComponent, HTMLComponent, APIComponent]] = []
