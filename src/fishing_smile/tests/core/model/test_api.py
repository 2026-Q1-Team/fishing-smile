import pytest
from sqlmodel import (
    select,
    delete,
    Session,
)
from fishing_smile.database.engine import get_session
from fishing_smile.core.model import *
from fishing_smile.core.fyke_hub import app
from fastapi.testclient import TestClient
from sqlalchemy import desc
import json

@pytest.fixture(name = 'client')
def fyke_hub_client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_change_password_api(session, client):
    profile = TargetProfileTable(
        name = 'test_change_password_api',
        email = 'test_change_password_api@nowhere.westeros.org',
    )
    attack = AttackTable(
        external_id = 'test_change_password_apitest_cha',
        scheme_name = 'generic_org_change_password',
        target = profile,
    )
    session.add(attack)
    session.flush()

    parameter = {"k": attack.external_id}
    response = client.get('/change_password', params = parameter)
    # test that it's the same for response and database. and it actually insert to database.
    statement = select(EventTable, AttackTable, TargetProfileTable).join(AttackTable, EventTable.parent_attack_id == AttackTable.id).join(TargetProfileTable, AttackTable.target_id == TargetProfileTable.id).order_by(EventTable.id.desc())
    result2 = session.exec(statement).first()
    session.refresh(profile)
    session.refresh(attack)
    #breakpoint()

    # test database match
    assert result2.TargetProfileTable.name == 'test_change_password_api'
    assert result2.TargetProfileTable.email == 'test_change_password_api@nowhere.westeros.org'
    assert result2.AttackTable.external_id == 'test_change_password_apitest_cha'
    assert result2.AttackTable.scheme_name == 'generic_org_change_password'
    assert result2.AttackTable.target.id == result2.TargetProfileTable.id
    assert result2.EventTable.kind == 'Email.sent, Link.clicked'
    assert result2.EventTable.detail == json.dumps({"ip": "testclient"})

    #
    assert str(response) == '<Response [200 OK]>'


def test_change_password_api2(session, client):
    profile = TargetProfileTable(
        name = 'test_change_password_api2',
        email = 'test_change_password_api2@nowhere.westeros.org',
    )
    attack = AttackTable(
        external_id = 'test_change_password_api2test_ch',
        scheme_name = 'generic_org_change_password',
        target = profile,
    )
    session.add(attack)
    session.flush()

    parameter_json = {'k': attack.external_id, 'p': 'password'}
    response = client.post('/api/change_password', json = parameter_json)

    # test that password is not plain password
    statement = select(EventTable, AttackTable, TargetProfileTable).join(AttackTable, EventTable.parent_attack_id == AttackTable.id).join(TargetProfileTable, AttackTable.target_id == TargetProfileTable.id).order_by(EventTable.id.desc())
    #breakpoint()
    result2 = session.exec(
        statement
    ).first()
    session.refresh(profile)
    session.refresh(attack)
    #breakpoint()

    # test database match
    assert result2.TargetProfileTable.name == 'test_change_password_api2'
    assert result2.TargetProfileTable.email == 'test_change_password_api2@nowhere.westeros.org'
    assert result2.AttackTable.external_id == 'test_change_password_api2test_ch'
    assert result2.AttackTable.scheme_name == 'generic_org_change_password'
    assert result2.AttackTable.target.id == result2.TargetProfileTable.id
    assert result2.EventTable.kind == "Email.sent, Link.clicked, Password.inserted"
    assert result2.EventTable.detail == '{"ip": "testclient", "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"}'


    #assert json.loads(response_json)["time"] == str(result.time) There is a milisecond issue. I will find a way around it to make it usable

