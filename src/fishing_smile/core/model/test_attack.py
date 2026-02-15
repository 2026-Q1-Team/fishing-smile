import pytest
from sqlmodel import (
    Session,
    select,
    delete,
)

from fishing_smile.database.engine import engine
from .target_profile import TargetProfile, TargetProfileTable
from .attack import Attack, AttackTable

from pprint import pprint

def test_create_refresh_cascade_delete():
    with Session(engine) as session:
        session.exec(delete(TargetProfileTable))
        session.exec(delete(AttackTable))

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

        session.rollback()
