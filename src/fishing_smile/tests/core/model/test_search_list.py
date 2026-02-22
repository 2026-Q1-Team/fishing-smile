from contextlib import nullcontext

import pytest
from pydantic import (
    BaseModel,
    ConfigDict,
)

from fishing_smile.core.model.search_list import SearchList


class FreeClass(BaseModel):
    model_config = ConfigDict(extra = 'allow')


@pytest.mark.parametrize(
    'items, conditions, expectation',
    [
        pytest.param(
            [
                {'name': 'first'},
                {'name': 'second'},
            ],
            {},
            nullcontext(
                {'name': 'first'},
            ),
            id = 'search without condition always get the first item',
        ),
        pytest.param(
            [
                {'kind': 'email', 'name': 'first'},
                {'kind': 'email', 'name': 'second'},
                {'kind': 'html', 'name': 'first'},
                {'kind': 'html', 'name': 'second'},
            ],
            {'kind': 'html'},
            nullcontext(
                {'kind': 'html', 'name': 'first'},
            ),
            id = 'search with one condition',
        ),
        pytest.param(
            [
                {'kind': 'email', 'name': 'first'},
                {'kind': 'email', 'name': 'second'},
                {'kind': 'html', 'name': 'first'},
                {'kind': 'html', 'name': 'second'},
            ],
            {'kind': 'html', 'name': 'second'},
            nullcontext(
                {'kind': 'html', 'name': 'second'},
            ),
            id = 'search with two condition',
        ),
        pytest.param(
            [
                {'name': 'first'},
                {'name': 'second'},
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
                FreeClass(id = 1),
                {'id': 2},
                FreeClass(id = 3),
                {'id': 4},
            ],
            {'id': 3},
            nullcontext(
                FreeClass(id = 3),
            ),
            id = 'match attributes if not a mapping',
        ),
        pytest.param(
            [
                FreeClass(kind = 'html'),
                FreeClass(name = 'second'),
                {'kind': 'email'},
                {'name': 'second'},
                FreeClass(kind = 'html', name = 'second'),
            ],
            {'kind': 'html', 'name': 'second'},
            nullcontext(
                FreeClass(kind = 'html', name = 'second'),
            ),
            id = 'missing key or attribute counts as not matching',
        ),
    ],
)
def test_first(items, conditions, expectation):
    items = SearchList(items)
    with expectation as expected:
        result = items.first(**conditions)
        assert result == expected
