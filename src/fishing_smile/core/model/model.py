from typing import (
    Annotated,
    List,
    Literal,
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
    kind: Literal['email']
    email_template: str


class HTMLComponent(AttackComponent):
    kind: Literal['html']
    url: str
    html_template: str


class APIComponent(AttackComponent):
    kind: Literal['api']
    url: str


AnyAttackComponent = Annotated[
    Union[EmailComponent, HTMLComponent, APIComponent],
    Field(discriminator = 'kind'),
]


class AttackScheme(BaseModel):
    name: str
    components: List[AnyAttackComponent] = []
