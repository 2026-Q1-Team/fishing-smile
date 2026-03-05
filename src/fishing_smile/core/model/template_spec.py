from typing import (
    Annotated,
    Literal,
    Union,
)
from pathlib import Path
import mimetypes

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
    _effective_path: Path
    _value: str

    @model_validator(mode = 'after')
    def read_template_value_from_file(self, info: ValidationInfo):
        if self.path.is_absolute():
            self._effective_path = self.path
        else:
            base_directory = info.context and info.context.get('base_directory', None)
            if base_directory is None:
                raise ValueError('Need base_directory context to resolve relative path to template file')
            self._effective_path = base_directory / self.path

        try:
            self._value = self._effective_path.read_text()
        except FileNotFoundError:
            raise ValueError(f'Path {self._effective_path} does not point to a file') from None
        return self

    @property
    def value(self) -> str:
        return self._value

    @model_validator(mode = 'after')
    def guess_type_when_not_explicitly_set(self):
        if 'mime' in self.model_fields_set:
            return self

        path = self._effective_path
        if path.suffix == '.jinja':
            path = path.with_suffix('')

        (guess, _) = mimetypes.guess_file_type(path)
        if guess:
            self.mime = guess
        return self


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
