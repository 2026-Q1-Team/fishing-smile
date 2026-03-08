from contextlib import nullcontext
from pathlib import Path

import pytest
from pydantic import (
    TypeAdapter,
    ValidationError,
)

from fishing_smile.settings import get_settings
from fishing_smile.core.model import *


_BASE_DIRECTORY = Path(__file__).parent.resolve() / 'test_cases/scheme/valid/scheme_with_external_template_file'


@pytest.mark.parametrize(
    'input_value, expectation',
    [
        pytest.param(
            'text {{ variable }}',
            nullcontext({
                'kind': 'string',
                'mime': 'text/plain',
                'value': 'text {{ variable }}',
            }),
            id = 'short template spec normalizes to StringTemplateSpec',
        ),
        pytest.param(
            {
                'kind': 'string',
                'mime': 'text/html',
                'value': '<html>{{ variable }}</html>',
            },
            nullcontext({
                'kind': 'string',
                'mime': 'text/html',
                'value': '<html>{{ variable }}</html>',
            }),
            id = 'long syntax used for specifying html mime type on string template',
        ),
        pytest.param(
            {
                'kind': 'file',
                'mime': 'text/javascript',
                'path': _BASE_DIRECTORY / 'script.js',
            },
            nullcontext({
                'kind': 'file',
                'mime': 'text/javascript',
                'path': _BASE_DIRECTORY / 'script.js',
                'value': 'alert(1);\n',
            }),
            id = 'specifying template using absolute path to file',
        ),
        pytest.param(
            {
                'kind': 'file',
                'mime': 'text/javascript',
                'path': 'non/existent/absolute/path/script.js',
            },
            pytest.raises(ValidationError),
            id = 'absolute path does not point to a file',
        ),
        pytest.param(
            {
                'kind': 'file',
                'mime': 'text/javascript',
                'path': 'script.js',
            },
            nullcontext({
                'kind': 'file',
                'mime': 'text/javascript',
                'path': Path('script.js'),
                'value': 'alert(1);\n',
                '_effective_path': _BASE_DIRECTORY / 'script.js',
            }),
            id = 'specifying template using relative path to file',
        ),
        pytest.param(
            {
                'kind': 'file',
                'mime': 'text/javascript',
                'path': 'non/existent/relative/path/script.js',
            },
            pytest.raises(ValidationError),
            id = 'relative path does not point to a file',
        ),
        pytest.param(
            {
                'kind': 'file',
                'path': 'script.js',
            },
            nullcontext({
                'kind': 'file',
                'mime': 'text/javascript',
                'path': Path('script.js'),
                'value': 'alert(1);\n',
            }),
            id = 'guess type',
        ),
        pytest.param(
            {
                'kind': 'file',
                'path': 'response.json.jinja',
            },
            nullcontext({
                'kind': 'file',
                'mime': 'application/json',
                'path': Path('response.json.jinja'),
                'value': '{"key":"value"}\n',
            }),
            id = 'guess type with jinja suffix',
        ),
        pytest.param(
            {
                'kind': 'file',
                'path': 'sub/no-extension',
            },
            nullcontext({
                'kind': 'file',
                'mime': 'text/plain',
                'path': Path('sub/no-extension'),
                'value': 'just text\n',
            }),
            id = 'leave guessable type as text/plain',
        ),
    ],
)
def test_template_spec(input_value, expectation):
    with expectation as expected_attrs:
        result = TypeAdapter(TemplateSpec).validate_python(
            input_value,
            context = {'base_directory': _BASE_DIRECTORY},
        )
        # NOTE: Not using model_dump() because `.value` is a private attribute in case of FileTemplateSpec
        result_attrs = {
            key: getattr(result, key)
            for key in expected_attrs
        }
        assert result_attrs == expected_attrs


def test_file_template_spec_cache():
    spec = TypeAdapter(TemplateSpec).validate_python(
        {
            'kind': 'file',
            'mime': 'text/javascript',
            'path': 'script.js',
        },
        context = {'base_directory': _BASE_DIRECTORY},
    )
    value_before = spec.value
    mtime_before = spec._value_mtime

    spec._effective_path.touch()
    value_after = spec.value
    mtime_after = spec._value_mtime
    if get_settings().deployment_mode == 'development':
        assert mtime_before != mtime_after
        # NOTE: The same immutable string object might be reused after reload. Can't test using string identity.
    else:
        assert mtime_before == mtime_after, 'Template auto-reloading is disabled in non-development mode'
        assert value_before is value_after
