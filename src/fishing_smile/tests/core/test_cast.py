from inspect import cleandoc
from email.mime.text import (
    MIMEText,
)

from sqlmodel import (
    select,
)

from fishing_smile.core.cast_net import (
    register_target_profile,
    register_new_attack,
    render_mail,
)
from fishing_smile.core.model import *
from fishing_smile.settings import (
    get_settings,
)


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


def test_render_mail(session):
    settings = get_settings()
    target = TargetProfileTable(
        name='John Fishing',
        email='address@domain.com',
        phone='0000000000',
        company='ocean gate',
        job_title='pro fisher',
    )
    attack = AttackTable(
        external_id='67',
        scheme_name='generic_org_survey',
        target_id='0',
        target = target,
    )
    msg = render_mail(target, attack)
    assert msg.as_string() == cleandoc("""
        Content-Type: text/html; charset="us-ascii"
        MIME-Version: 1.0
        Content-Transfer-Encoding: 7bit
        Subject: ocean gate Yearly Benefits Survey.
        From: siw013061@gmail.com
        To: address@domain.com

        Dear John Fishing,

        We would like to gather feedback from all members of the pro fisher team,
        in order to improve the quality of benefits we provide to our employees.

        Please fill out the form below.

        <a href="localhost/index.html?k=67"><img src=""></a>

        Thank you for taking your time to improve our organization.
        - HR Team.
    """)
