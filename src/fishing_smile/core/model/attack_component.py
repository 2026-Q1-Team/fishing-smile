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
    templates: dict[str, str] = {}


class EmailComponent(AttackComponent):
    kind: Literal['email'] = 'email'
    foo: str = 'bar'
    # TODO: Required templates:
    # - subject
    # - body


# NOTE: Maybe we should have a `handler` property that
# evaluates to a FastAPI endpoint definition.
# The `handler` could be populated through naming python module
# or ...
# NOTE: And if we have `handler` property,
# both HTML and API can be handled the same way.
class HTMLComponent(AttackComponent):
    kind: Literal['html'] = 'html'
    # TODO: Required templates:
    # - url
    # - html


class APIComponent(AttackComponent):
    kind: Literal['api'] = 'api'
    # TODO: Required templates:
    # - url
