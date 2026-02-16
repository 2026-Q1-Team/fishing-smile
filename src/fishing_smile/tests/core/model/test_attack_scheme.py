from pathlib import Path

import pytest
import yaml

from fishing_smile.core.model import *


@pytest.mark.parametrize(
    'scheme_file',
    list((Path(__file__).parent / 'test_cases/scheme').glob('*.yaml')),
)
def test_create_attack_scheme(scheme_file):
    scheme_name = scheme_file.stem
    with open(scheme_file) as f:
        doc = yaml.safe_load(f)
    scheme = AttackScheme.model_validate(doc)
    assert scheme.name == scheme_name
