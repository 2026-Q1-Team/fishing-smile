from sqlmodel import (
    select,
)

from fishing_smile.core.cast_net import (
    register_target_profile,
    register_new_attack,
)
from fishing_smile.core.model import *


def test_upsert_on_same_email(session):
    old_profile = TargetProfile(
        name = 'Gandalf the Grey',
        email = 'gandalf@middle.earth.org',
    )
    registered_old_profile = register_target_profile(old_profile, session)
    new_profile = TargetProfile(
        name = 'Gandalf the White',
        email = 'gandalf@middle.earth.org',
        phone = '0123456789',
    )
    expected = new_profile.model_dump(exclude = ['id'])
    registered_new_profile = register_target_profile(new_profile, session)
    assert registered_old_profile is registered_new_profile, \
        'Registering profiles with duplicate email should result in the same object'

    results = session.exec(
        select(TargetProfileTable)
    ).all()

    assert len(results) == 1
    assert results[0] is registered_old_profile
    assert results[0].model_dump(exclude = ['id']) == expected


def test_register_new_attack(session):
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
    out = register_new_attack(target, scheme, session)
    result_profile = session.exec(select(TargetProfileTable).where(TargetProfileTable.name == target.name)).all()
    result_attack = session.exec(select(AttackTable).where(AttackTable.external_id == out.external_id)).all()
    assert len(result_attack) == 1
    assert result_profile[0].id == result_attack[0].target_id


def test_send_mail(session):
    # TODO -- what should the send mail function return that can prove the mail was received not just sent?
    assert 1 == 1
