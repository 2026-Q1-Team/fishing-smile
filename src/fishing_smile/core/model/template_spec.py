from typing import (
    Annotated,
    Literal,
    Union,
    Callable,
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
from jinja2 import Template

from fishing_smile.settings import get_settings
from .always_equal import AlwaysEqual


class LongTemplateSpec(BaseModel):
    kind: str
    mime: str = 'text/plain'
    _jinja: AlwaysEqual[Callable[[], Template]] | None = None

    @property
    def jinja(self) -> Template:
        return self._jinja.value()


class StringTemplateSpec(LongTemplateSpec):
    kind: Literal['string'] = 'string'
    value: str


class FileTemplateSpec(LongTemplateSpec):
    kind: Literal['file'] = 'file'
    path: Path
    _effective_path: Path
    _value: str
    _value_mtime: float

    @model_validator(mode = 'after')
    def resolve_path(self, info: ValidationInfo):
        if self.path.is_absolute():
            self._effective_path = self.path
        else:
            base_directory = info.context and info.context.get('base_directory', None)
            if base_directory is None:
                raise ValueError('Need base_directory context to resolve relative path to template file')
            self._effective_path = base_directory / self.path
        return self

    @model_validator(mode = 'after')
    def reload_from_file(self):
        try:
            current_mtime = self._effective_path.stat().st_mtime
            previous_mtime = getattr(self, '_value_mtime', None)
            if current_mtime != previous_mtime:
                self._value_mtime = current_mtime
                self._value = self._effective_path.read_text()
        except FileNotFoundError:
            raise ValueError(f'Path {self._effective_path} does not point to a file') from None
        return self

    @property
    def value(self) -> str:
        if get_settings().deployment_mode == 'development':
            self.reload_from_file()
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
