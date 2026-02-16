import pytest
from sqlmodel import (
    select,
    delete,
)

from fishing_smile.core.model import *


def test_create_search_delete(session):
    profile = TargetProfileTable(
        name = 'Jon Snow',
        email = 'jon.snow@nowhere.westeros.org',
    )
    attack = AttackTable(
        external_id = '01234567890123456789012345678901',
        scheme_name = 'empty',
        target = profile,
    )
    event = EventTable(
        parent_attack = attack,
        kind = 'ping',
    )
    session.add(event)

    results = session.exec(select(EventTable)).all()
    assert len(results) == 1
    assert results[0].parent_attack == attack
    assert results[0].parent_attack.events == [results[0]]

    session.exec(delete(EventTable))
    results = session.exec(select(EventTable)).all()
    assert len(results) == 0
    results = session.exec(select(AttackTable)).all()
    assert results[0].scheme_name == 'empty'
