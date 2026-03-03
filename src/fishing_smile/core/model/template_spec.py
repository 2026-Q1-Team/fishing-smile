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
    ValidationInfo,
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
    @model_validator(mode = "after")
    def read_template_value_from_file(self, info: ValidationInfo):
        if self.path.is_absolute():
            effective_path = self.path
        else:
            base_directory = info.context and info.context.get('base_directory', None)
            if base_directory is None:
                raise ValueError('Need base_directory context to resolve relative path to template file')
            effective_path = base_directory / self.path

        try:
            self._value = effective_path.read_text()
        except FileNotFoundError:
            raise ValueError(f'Path {effective_path} does not point to a file') from None
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
