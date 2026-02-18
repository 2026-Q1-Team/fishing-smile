from sqlmodel import (
    select,
)

from fishing_smile.core.cast_net import update_database
from fishing_smile.core.model import *


def test_update_db(session):
    target = TargetProfile(
        name='John Fishing',
        email='address@domail.com',
        phone=0000000000,
        company='ocean gate',
        job_title='pro fisher',
    )
    ex_id_out = update_database(target, 'update_test', session)
    result_profile = session.exec(select(TargetProfileTable).where(TargetProfileTable.name == target.name))
    result_attack = session.exec(select(AttackTable).where(AttackTable.external_id == ex_id_out))
    assert len(result_attack) == 1
    assert result_profile[0].id == result_attack[0].target_id


def test_send_mail():
    assert 1 == 1
