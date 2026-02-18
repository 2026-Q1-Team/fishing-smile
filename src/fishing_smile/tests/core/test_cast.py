from sqlmodel import (
    select,
)

from fishing_smile.core.cast_net import update_database
from fishing_smile.core.model import *


def test_update_db(session):
    target = TargetProfile(
        name = 'John Fishing',
        email = 'address@domail.com',
        phone = '0000000000',
        company = 'ocean gate',
        job_title = 'pro fisher',
    )
    ex_id_out = update_database(target, 'update_test', session)
    result_attacks = session.exec(select(AttackTable)).all()
    assert len(result_attacks) == 1
    assert result_attacks[0].scheme_name == 'update_test'
    assert result_attacks[0].target.email == 'address@domail.com'


def test_send_mail():
    assert 1 == 1
