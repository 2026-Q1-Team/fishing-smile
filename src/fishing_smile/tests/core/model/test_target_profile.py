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


# TODO: Skip if engine is not using mysql or mariadb
# NOTE: Not sure if we will use this upsert pattern, but just making sure it works.
# - pros: use sqlmodel and execute only in single SQL statement
# - cons: verbose, use MySQL specific interface
def test_upsert_on_same_email(session):
    from sqlalchemy.dialects.mysql import insert
    old_profile = TargetProfileTable(
        name = 'Gandalf the Grey',
        email = 'gandalf@middle.earth.org',
    )
    session.add(old_profile)
    new_profile = TargetProfileTable(
        name = 'Gandalf the White',
        email = 'gandalf@middle.earth.org',
        phone = '0123456789',
    )
    session.exec(
        insert(TargetProfileTable).values(
            name = new_profile.name,
            phone = new_profile.phone,
            email = new_profile.email,
            company = new_profile.company,
            job_title = new_profile.job_title,
        ).on_duplicate_key_update(
            name = new_profile.name,
            phone = new_profile.phone,
            company = new_profile.company,
            job_title = new_profile.job_title,
        )
    )

    results = session.exec(
        select(TargetProfileTable)
    ).all()
    # NOTE: It's a bit confusing how results returned from select is actually
    # the old_profile object which has NOT been refreshed yet.
    # I guess there is an internal object pool in sqlmodel that de-duplicate objects by primary key.
    assert len(results) == 1
    assert results[0] is old_profile
    assert old_profile is not new_profile
    assert old_profile != new_profile
    # Only after the returned object is refreshed, then their content (except id) will be the same.
    session.refresh(results[0])
    for k,v in results[0].model_dump().items():
        if k == 'id':
            continue
        assert v == getattr(new_profile, k)
    # NOTE: new_profile can't be refreshed because it's outside of sqlmodel session management
