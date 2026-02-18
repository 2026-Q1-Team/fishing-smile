import pytest
from sqlmodel import (
    select,
    delete,
)
from pydantic import ValidationError

from fishing_smile.core.model import *


def test_create_search_delete(session):
    before = session.exec(
        select(TargetProfileTable)
    ).all()
    assert len(before) == 0
    profile = TargetProfileTable(
        name = 'Jon Snow',
        email = 'jon.snow@nowhere.westeros.org',
    )
    assert profile.name == 'Jon Snow'
    session.add(profile)
    results = session.exec(
        select(TargetProfileTable).where(TargetProfileTable.name == 'Jon Snow')
    ).all()
    assert len(results) == 1
    assert results[0].email == 'jon.snow@nowhere.westeros.org'


def test_invalid_email():
    with pytest.raises(ValidationError):
        profile = TargetProfile(
            name = 'Jon Snow',
            email = 'invalid-because-it-does-not-have-at-sign',
        )
    # NOTE: "Table" models does not validate in constructor, must explicitly use `.model_validate()`
    with pytest.raises(ValidationError):
        profile = TargetProfileTable.model_validate({
            'name': 'Jon Snow',
            'email': 'invalid-because-it-does-not-have-at-sign',
        })


def test_phone_number_too_long():
    with pytest.raises(ValidationError):
        profile = TargetProfile(
            name = 'Jon Snow',
            email = 'jon.snow@nowhere.westeros.org',
            phone = '01234567890123456789',
        )
