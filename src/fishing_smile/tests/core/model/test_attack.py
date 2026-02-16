import pytest
from sqlmodel import (
    select,
    delete,
)

from fishing_smile.core.model import *


def test_create_search_cascade_delete(session):
    profile = TargetProfileTable(
        name = 'Jon Snow',
        email = 'jon.snow@nowhere.westeros.org',
    )
    attack = AttackTable(
        external_id = '01234567890123456789012345678901',
        scheme_name = 'empty',
        target = profile,
    )
    session.add(attack)

    results = session.exec(
        select(AttackTable)
            .where(AttackTable.external_id == '01234567890123456789012345678901')
    ).all()
    assert len(results) == 1
    assert results[0].scheme_name == 'empty'
    assert results[0].target_id == results[0].target.id
    assert results[0].target.attacks == [results[0]]

    session.exec(delete(TargetProfileTable))
    results = session.exec(select(AttackTable)).all()
    assert len(results) == 0, \
        'deletion of TargetProfile should cascade to Attack'
