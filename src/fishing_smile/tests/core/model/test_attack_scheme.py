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
