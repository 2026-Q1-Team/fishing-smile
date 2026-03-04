import pytest

from fishing_smile.core.model import *


@pytest.mark.parametrize(
    'scheme_name',
    list(standard_schemes.schemes),
)
def test_get_standard_schemes(scheme_name):
    scheme = standard_schemes.get(scheme_name)
    assert scheme.name == scheme_name


def test_get_scheme_name_not_indexed_in_standard_collection():
    with pytest.raises(ValueError, match = 'not indexed'):
        scheme = standard_schemes.get('scheme_does_not_exist')
