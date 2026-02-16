from pathlib import Path

import pytest
import yaml

from fishing_smile.core.model import *


@pytest.mark.parametrize(
    'scheme_name',
    [
        'empty',
        'change_password',
    ]
)
def test_create_attack_scheme(scheme_name):
    path = Path(__file__).parent / f'test_cases/scheme/{scheme_name}.yaml'
    with open(path) as f:
        doc = yaml.safe_load(f)
    scheme = AttackScheme.model_validate(doc)
    assert scheme.name == scheme_name
