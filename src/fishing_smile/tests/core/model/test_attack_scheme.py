from pathlib import Path
from contextlib import nullcontext

import pytest
import yaml
from pydantic import ValidationError

from fishing_smile.core.model import *


TEST_SCHEME_PATH = Path(__file__).parent / 'test_cases/scheme'


@pytest.mark.parametrize(
    'scheme_file',
    list(TEST_SCHEME_PATH.glob('valid/*.yaml')),
)
def test_create_attack_scheme(scheme_file):
    scheme_name = scheme_file.stem
    with open(scheme_file) as f:
        doc = yaml.safe_load(f)
    scheme = AttackScheme.model_validate(doc)
    assert scheme.name == scheme_name


@pytest.mark.parametrize(
    'scheme_file',
    list(TEST_SCHEME_PATH.glob('invalid/*.yaml')),
)
def test_invalid_attack_scheme(scheme_file):
    with pytest.raises(ValidationError):
        with open(scheme_file) as f:
            doc = yaml.safe_load(f)
        scheme = AttackScheme.model_validate(doc)


@pytest.mark.parametrize(
    'scheme_name',
    AttackScheme.list(),
)
def test_get_registered_schemes(scheme_name):
    scheme = AttackScheme.get(scheme_name)
    assert scheme.name == scheme_name


@pytest.mark.parametrize(
    'components, search, expectation',
    [
        pytest.param(
            [
                EmailComponent(name = 'first', email_template = ''),
                EmailComponent(name = 'second', email_template = ''),
            ],
            {},
            nullcontext(
                EmailComponent(name = 'first', email_template = ''),
            ),
            id = 'without search condition, get first component',
        ),
        pytest.param(
            [
                APIComponent(name = 'login', url = ''),
                EmailComponent(name = 'first', email_template = ''),
                EmailComponent(name = 'second', email_template = ''),
            ],
            {'name': 'second'},
            nullcontext(
                EmailComponent(name = 'second', email_template = ''),
            ),
            id = 'search only by name',
        ),
        pytest.param(
            [
                APIComponent(name = 'login', url = ''),
                EmailComponent(name = 'first', email_template = ''),
                EmailComponent(name = 'second', email_template = ''),
            ],
            {'name': 'third'},
            pytest.raises(ValueError),
            id = 'search not found',
        ),
        pytest.param(
            [],
            {},
            pytest.raises(ValueError),
            id = 'search not found on empty list',
        ),
        pytest.param(
            [
                APIComponent(name = 'login', url = ''),
                HTMLComponent(name = 'login', url = '', html_template = ''),
            ],
            {'name': 'login', 'kind': 'html'},
            nullcontext(
                HTMLComponent(name = 'login', url = '', html_template = ''),
            ),
            id = 'search by both name and kind',
        ),
    ],
)
def test_find_component(components, search, expectation):
    scheme = AttackScheme(
        name = 'scheme_name',
        components = components,
    )
    with expectation as expected:
        result = scheme.find_component(**search)
        assert result == expected
