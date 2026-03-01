from pathlib import Path

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


def test_get_invalid_scheme_name():
    with pytest.raises(ValueError, match = 'not a valid attack scheme name'):
        scheme = AttackScheme.get('scheme_does_not_exist')


def test_find_component():
    expected = HTMLComponent(name = 'first', url = '', html_template = '')
    scheme = AttackScheme(
        name = 'scheme_name',
        components = [
            EmailComponent(name = 'first', email_template = ''),
            EmailComponent(name = 'second', email_template = ''),
            expected,
        ],
    )
    result = scheme.components.first(kind = 'html', name = 'first')
    assert result == expected
