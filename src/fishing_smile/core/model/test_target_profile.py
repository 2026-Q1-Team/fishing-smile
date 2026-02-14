import pytest
from sqlmodel import (
    Session,
    select,
    delete,
)

from fishing_smile.database.engine import engine
from .target_profile import TargetProfile


def test_create_search_delete():
    with Session(engine) as session:
        session.exec(delete(TargetProfile))
        before = session.exec(
            select(TargetProfile)
        ).all()
        assert len(before) == 0
        profile = TargetProfile(
            name = 'Jon Snow',
            email = 'jon.snow@nowhere.westeros.org',
        )
        assert profile.name == 'Jon Snow'
        session.add(profile)
        results = session.exec(
            select(TargetProfile).where(TargetProfile.name == 'Jon Snow')
        ).all()
        assert len(results) == 1
        assert results[0].email == 'jon.snow@nowhere.westeros.org'
        session.rollback()
