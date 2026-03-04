from typing import (
    Literal,
)

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)

from .red_flag import RedFlag
from .template_spec import TemplateSpec


class AttackComponent(BaseModel):
    model_config = ConfigDict(extra = 'allow')
    kind: str
    name: str
    red_flags: list[RedFlag] = []
    templates: dict[str, TemplateSpec] = {}


class EmailTemplate(BaseModel):
    model_config = ConfigDict(extra = 'allow')
    subject: TemplateSpec
    body: TemplateSpec

class EmailComponent(AttackComponent):
    kind: Literal['email'] = 'email'
    email_template: str | None = None
    template: EmailTemplate


# NOTE: Maybe we should have a `handler` property that
# evaluates to a FastAPI endpoint definition.
# The `handler` could be populated through naming python module
# or ...
# NOTE: And if we have `handler` property,
# both HTML and API can be handled the same way.
class HTMLComponent(AttackComponent):
    kind: Literal['html'] = 'html'
    url: TemplateSpec
    html_template: TemplateSpec


class APIComponent(AttackComponent):
    kind: Literal['api'] = 'api'
    url: TemplateSpec
