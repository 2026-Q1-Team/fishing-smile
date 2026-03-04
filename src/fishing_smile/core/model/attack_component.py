from typing import (
    Literal,
    ClassVar,
)
from http import HTTPMethod

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
)

from .red_flag import RedFlag
from .template_spec import TemplateSpec


class AttackComponent(BaseModel):
    model_config = ConfigDict(extra = 'allow')
    kind: str
    name: str
    red_flags: list[RedFlag] = []
    templates: dict[str, TemplateSpec] = Field(
        {},
        validate_default = True,
    )

    # Define what keys are required in `templates` field.
    # Subclass can set a new value for this class variable.
    required_templates: ClassVar[list[str]] = []

    @field_validator('templates', mode = 'after')
    @classmethod
    def check_required_templates(cls, templates):
        for required in cls.required_templates:
            if required not in templates:
                raise ValueError(f'{required} template is required')
        return templates


class EmailComponent(AttackComponent):
    kind: Literal['email'] = 'email'
    #required_templates = ['subject', 'body']


# NOTE: Maybe we should have a `handler` property that
# evaluates to a FastAPI endpoint definition.
# The `handler` could be populated through naming python module
# or ...
# NOTE: And if we have `handler` property,
# both HTML and API can be handled the same way.
class HTMLComponent(AttackComponent):
    kind: Literal['html'] = 'html'
    required_templates = ['url', 'html']


class APIComponent(AttackComponent):
    kind: Literal['api'] = 'api'
    method: HTTPMethod = 'POST'
    required_templates = ['url']
