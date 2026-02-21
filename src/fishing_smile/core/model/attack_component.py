from typing import (
    List,
    Literal,
)

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)

from .red_flag import RedFlag


class AttackComponent(BaseModel):
    model_config = ConfigDict(extra = 'allow')

    kind: str
    name: str
    red_flags: List[RedFlag] = []


class EmailComponent(AttackComponent):
    kind: Literal['email'] = 'email'
    email_template: str


# NOTE: Maybe we should have a `handler` property that
# evaluates to a FastAPI endpoint definition.
# The `handler` could be populated through naming python module
# or ...
# NOTE: And if we have `handler` property,
# both HTML and API can be handled the same way.
class HTMLComponent(AttackComponent):
    kind: Literal['html'] = 'html'
    url: str
    html_template: str


class APIComponent(AttackComponent):
    kind: Literal['api'] = 'api'
    url: str
