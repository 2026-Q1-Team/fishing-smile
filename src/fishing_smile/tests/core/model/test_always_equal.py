import pytest
from pydantic import (
    BaseModel,
    ConfigDict,
)

from fishing_smile.core.model.always_equal import AlwaysEqual


def test_eq():
    one = AlwaysEqual(1)
    two = AlwaysEqual(2)
    assert one == two
    assert one.value != two.value


def test_hash():
    one = AlwaysEqual(1)
    two = AlwaysEqual(2)
    d = { one, two }
    assert len(d) == 1


def test_pydantic_model_equality_ignore_always_equal_private_field():
    class Item(BaseModel):
        name: str
        _created_by: AlwaysEqual[str]

        @classmethod
        def create(cls, by: str, /, **kwargs):
            item = cls(**kwargs)
            item._created_by = AlwaysEqual(by)
            return item

    one = Item.create('one', name = 'Martha')
    two = Item.create('two', name = 'Martha')
    assert one == two
    assert one._created_by == two._created_by
    assert one._created_by.value != two._created_by.value

    different = Item.create('one', name = 'Matilda')
    assert one != different


def test_pydantic_model_hash_ignore_always_equal_private_field():
    class Item(BaseModel):
        model_config = ConfigDict(frozen = True)
        name: str
        _created_by: AlwaysEqual[str]

        @classmethod
        def create(cls, by: str, /, **kwargs):
            item = cls(**kwargs)
            item._created_by = AlwaysEqual(by)
            return item

    one = Item.create('one', name = 'Martha')
    two = Item.create('two', name = 'Martha')
    different = Item.create('one', name = 'Matilda')
    assert hash(one) == hash(two)
    assert hash(one) != hash(different)
