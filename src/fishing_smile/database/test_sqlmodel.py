import pytest
from sqlmodel import Field

from .sqlmodel import (
    to_snake_case,
    SQLModel,
)


@pytest.mark.parametrize(
    'name, expected',
    [
        (
            'already_snake_case',
            'already_snake_case',
        ),
        (
            'PascalCase',
            'pascal_case',
        ),
        (
            'camelCase',
            'camel_case',
        ),
    ]
)
def test_to_snake_case(name, expected):
    result = to_snake_case(name)
    assert result == expected


def test_sqlmodel():
    class SomeObjectTable(SQLModel, table = True):
        id: int = Field(primary_key = True)
    assert SomeObjectTable.__tablename__ == 'some_object'
