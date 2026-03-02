from typing import (
    Annotated,
    Literal,
    Union,
)
from pathlib import Path

from pydantic import (
    BaseModel,
    Field,
    model_validator,
    BeforeValidator,
)


class LongTemplateSpec(BaseModel):
    kind: str
    mime: str = 'text/plain'


class StringTemplateSpec(LongTemplateSpec):
    kind: Literal['string'] = 'string'
    value: str


class FileTemplateSpec(LongTemplateSpec):
    kind: Literal['file'] = 'file'
    path: Path
    # NOTE: This is a private field used to cache file content
    _value: str

    # TODO: guess mime type from filename 
    @model_validator(mode="after")
    def read_template_value_from_file(self):
        try:
            # TODO: support relative path
            self._value = self.path.read_text()
        except FileNotFoundError:
            raise ValueError('Path does not point to a file') from None
        return self

    @property
    def value(self) -> str:
        return self._value


AnyLongTemplateSpec = Annotated[
    Union[StringTemplateSpec, FileTemplateSpec],
    Field(discriminator = 'kind'),
]


def _normalize_str_to_long_spec(x):
    if not isinstance(x, str):
        return x
    return StringTemplateSpec(value = x)


TemplateSpec = Annotated[
    str | AnyLongTemplateSpec,
    BeforeValidator(_normalize_str_to_long_spec),
]
