from sqlmodel import (
    select,
)

from fishing_smile.core.cast_net import update_database
from fishing_smile.core.model import *


def test_update_db(session):
    scheme = AttackScheme(
        name='test_scheme_1',
        description='this is a test'
    )
    target = TargetProfileTable(
        name='John Fishing',
        email='address@domain.com',
        phone='0000000000',
        company='ocean gate',
        job_title='pro fisher',
    )
    out = update_database(target, scheme, session)
    result_profile = session.exec(select(TargetProfileTable).where(TargetProfileTable.name == target.name)).all()
    result_attack = session.exec(select(AttackTable).where(AttackTable.external_id == out.external_id)).all()
    assert len(result_attack) == 1
    assert result_profile[0].id == result_attack[0].target_id


def test_send_mail():
    assert 1 == 1
