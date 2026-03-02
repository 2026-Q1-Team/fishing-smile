from contextlib import nullcontext
from pathlib import Path

import pytest
from pydantic import (
    TypeAdapter,
    ValidationError,
)

from fishing_smile.core.model import *


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
                'path': Path(__file__).parent.resolve() / 'test_cases/scheme/valid/scheme_with_external_template_file/script.js',
            },
            nullcontext({
                'kind': 'file',
                'mime': 'text/javascript',
                'path': Path(__file__).parent.resolve() / 'test_cases/scheme/valid/scheme_with_external_template_file/script.js',
                'value': 'alert(1);\n',
            }),
            id = 'specifying template using absolute path to file',
        ),
        pytest.param(
            {
                'kind': 'file',
                'mime': 'text/javascript',
                'path': 'non/existent/path/script.js',
            },
            pytest.raises(ValidationError),
            id = 'path does not point to a file',
        ),
    ],
)
def test_template_spec(input_value, expectation):
    with expectation as expected_attrs:
        result = TypeAdapter(TemplateSpec).validate_python(input_value)
        result_attrs = {
            key: getattr(result, key)
            for key in expected_attrs
        }
        assert result_attrs == expected_attrs
