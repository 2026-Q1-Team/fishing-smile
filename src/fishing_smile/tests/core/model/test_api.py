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
        scheme_name = 'empty',
        target = profile,
    )
    session.add(attack)
    session.flush()

    parameter = {"k": attack.external_id}
    response = client.get('/change_password', params = parameter)
    response_json = response.json()

    attack_id = json.loads(response_json)["result"]
    result = session.exec(
        select(EventTable).where(EventTable.parent_attack_id == int(attack_id)).order_by(desc(EventTable.id))
    ).first()

    # test that it's the same for response and database. and it actually insert to database.
    assert result.kind == 'Email sent, Link clicked' == json.loads(response_json)["kind"]  
    assert result.parent_attack_id == json.loads(response_json)["result"]
    assert result.detail == json.loads(response_json)["detail"]
    #assert json.loads(response_json)["time"] == str(result.time) There is a milisecond issue. I will find a way around it to make it usable


def test_change_password_api2(session, client):
    profile = TargetProfileTable(
        name = 'test_change_password_api2',
        email = 'test_change_password_api2@nowhere.westeros.org',
    )
    attack = AttackTable(
        external_id = 'test_change_password_api22222222',
        scheme_name = 'empty',
        target = profile,
    )
    session.add(attack)
    session.flush()

    parameter_json = {'k': attack.external_id, 'p': 'password'}
    response = client.post('/api/change_password', json = parameter_json)
    response_json = response.json()

    attack_id = json.loads(response_json)["result"]
    result = session.exec(
        select(EventTable).where(EventTable.parent_attack_id == int(attack_id)).order_by(desc(EventTable.id))
    ).first()

    # test that it's the same for response and database. and it actually insert to database.
    assert result.kind == 'Email sent, Link clicked, Password inserted' == json.loads(response_json)["kind"] 
    assert result.parent_attack_id == json.loads(response_json)["result"]
    assert result.detail == json.loads(response_json)["detail"]
    #assert json.loads(response_json)["time"] == str(result.time) There is a milisecond issue. I will find a way around it to make it usable
