from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from fishing_smile.core.model import *


TEST_SCHEME_PATH = Path(__file__).parent / 'test_cases/scheme'


@pytest.mark.parametrize(
    'scheme_file',
    list(TEST_SCHEME_PATH.glob('valid/**/*.yaml')),
    ids = (lambda path: str(path.relative_to(TEST_SCHEME_PATH))),
)
def test_create_valid_attack_schemes_from_file(scheme_file):
    scheme = AttackScheme.from_file(scheme_file)


@pytest.mark.parametrize(
    'scheme_file',
    list(TEST_SCHEME_PATH.glob('invalid/**/*.yaml')),
    ids = (lambda path: str(path.relative_to(TEST_SCHEME_PATH))),
)
def test_create_invalid_attack_schemes_from_file(scheme_file):
    with pytest.raises(ValidationError):
        scheme = AttackScheme.from_file(scheme_file)


def test_find_component():
    expected = HTMLComponent(
        name = 'first',
        templates = {
            'url': '',
            'html': '<html></html>',
        },
    )
    scheme = AttackScheme(
        name = 'scheme_name',
        components = [
            EmailComponent(name = 'first', templates = {'subject': '', 'body': ''}),
            EmailComponent(name = 'second', templates = {'subject': '', 'body': ''}),
            expected,
        ],
    )
    result = scheme.components.first(kind = 'html', name = 'first')
    assert result == expected


def test_component_must_have_unique_kind_name_pair():
    # NOTE: same name is allowed if components are of different kind
    scheme = AttackScheme(
        name = 'scheme_name',
        components = [
            EmailComponent(name = 'same_name', templates = {'subject': '', 'body': ''}),
            HTMLComponent(name = 'same_name', templates = {'url': '', 'html': ''}),
        ],
    )
    with pytest.raises(ValidationError, match = 'components within a scheme must have unique kind-name pair'):
        scheme = AttackScheme(
            name = 'scheme_name',
            components = [
                EmailComponent(name = 'same_name', templates = {'subject': 'hello', 'body': ''}),
                EmailComponent(name = 'same_name', templates = {'subject': 'bye', 'body': ''}),
            ],
        )
