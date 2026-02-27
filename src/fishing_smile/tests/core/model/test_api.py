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

    profile2 = TargetProfileTable(
        name = 'John Fishing',
        email = 'John.Fishing@nowhere.westeros.org',
    )
    attack2 = AttackTable(
        external_id = 'test_change_password_api_John_Fi',
        scheme_name = 'scheme12345',
        target = profile2,
    )
    session.add(attack)
    session.add(attack2)
    session.flush()

    parameter = {"k": attack.external_id}
    response = client.get('/change_password', params = parameter)
    statement = select(EventTable, AttackTable, TargetProfileTable).join(AttackTable, EventTable.parent_attack_id == AttackTable.id).join(TargetProfileTable, AttackTable.target_id == TargetProfileTable.id).order_by(EventTable.id.desc())
    result2 = session.exec(statement).first()
    session.refresh(profile)
    session.refresh(attack)

    # test database match
    assert result2.TargetProfileTable.name == 'test_change_password_api',\
        "TargetProfileTable.name between database and test doesn't match"
    assert result2.TargetProfileTable.email == 'test_change_password_api@nowhere.westeros.org',\
        "TargetProfileTable.email between database and test doesn't match"
    assert result2.AttackTable.external_id == 'test_change_password_apitest_cha',\
        "AttackTable.external_id between database and test doesn't match"
    assert result2.AttackTable.scheme_name == 'generic_org_change_password',\
        "AttackTable.scheme_name between database and test doesn't match"
    assert result2.AttackTable.target.id == result2.TargetProfileTable.id ,\
        "AttackTable.target.id between database and test doesn't match"
    assert result2.EventTable.kind == 'Email.sent, Link.clicked',\
        "EventTable.kind between database and test doesn't match"
    assert result2.EventTable.detail == json.dumps({"ip": "testclient", "attack_scheme": "generic_org_change_password"}),\
        "EventTable.detail between database and test doesn't match"
    assert str(response) == '<Response [200 OK]>',\
        "HTTP response between database and test doesn't match"

    session.refresh(attack2)
    parameter = {"k": attack2.external_id}
    response = client.get('/change_password', params = parameter)

    # test condition when attack scheme is invalid
    assert str(response) == '<Response [404 Not Found]>',\
        "test case for invalid attack scheme doesn't give HTTP respionse <Response [404 Not Found]>"



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
    profile2 = TargetProfileTable(
        name = 'John Fishing',
        email = 'John.Fishing@nowhere.westeros.org',
    )
    attack2 = AttackTable(
        external_id = 'test_change_password_api_John_Fi',
        scheme_name = 'scheme12345',
        target = profile2,
    )
    session.add(attack)
    session.add(attack2)
    session.flush()

    parameter_json = {'k': attack.external_id, 'p': 'password'}
    response = client.post('/api/change_password', json = parameter_json)

    statement = select(EventTable, AttackTable, TargetProfileTable).join(AttackTable, EventTable.parent_attack_id == AttackTable.id).join(TargetProfileTable, AttackTable.target_id == TargetProfileTable.id).order_by(EventTable.id.desc())

    result2 = session.exec(
        statement
    ).first()
    session.refresh(profile)
    session.refresh(attack)

    # test database match
    assert result2.TargetProfileTable.name == 'test_change_password_api2',\
        "TargetProfileTable.name between database and test doesn't match"
    assert result2.TargetProfileTable.email == 'test_change_password_api2@nowhere.westeros.org',\
        "TargetProfileTable.email between database and test doesn't match"
    assert result2.AttackTable.external_id == 'test_change_password_api2test_ch',\
        "AttackTable.external_id between database and test doesn't match"
    assert result2.AttackTable.scheme_name == 'generic_org_change_password',\
        "AttackTable.scheme_name between database and test doesn't match"
    assert result2.AttackTable.target.id == result2.TargetProfileTable.id ,\
        "AttackTable.target.id between database and test doesn't match"
    assert result2.EventTable.kind == "Email.sent, Link.clicked, Password.inserted",\
        "EventTable.kind between database and test doesn't match"
    assert result2.EventTable.detail == '{"ip": "testclient", "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", "attack_scheme": "generic_org_change_password"}',\
        "EventTable.detail between database and test doesn't match"

    session.refresh(attack2)
    parameter_json2 = {'k': attack2.external_id, 'p': 'password'}
    response = client.post('/api/change_password', json = parameter_json2)

    # test condition when attack scheme is invalid
    assert str(response) == '<Response [404 Not Found]>',\
        "test case for invalid attack scheme doesn't give HTTP respionse <Response [404 Not Found]>"
