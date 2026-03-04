import pytest
from sqlmodel import (
    select,
)
from fastapi.testclient import TestClient

from fishing_smile.database.engine import get_session
from fishing_smile.core.model import *
from fishing_smile.core.fyke_hub import app


@pytest.fixture(name = 'client')
def fyke_hub_client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_change_password_page(session, client):
    attacks = [
        AttackTable(
            external_id = 'test_change_password_html_page_1',
            scheme_name = 'generic_org_change_password',
            target = TargetProfileTable(
                name = 'Jack Fishing',
                email = 'jack.fishing@nowhere.westeros.org',
            ),
        ),
        AttackTable(
            external_id = 'test_change_password_html_page_2',
            scheme_name = 'invalid_scheme',
            target = TargetProfileTable(
                name = 'John Fishing',
                email = 'John.Fishing@nowhere.westeros.org',
            ),
        ),
    ]
    session.add_all(attacks)
    session.flush()

    parameter = {"k": attacks[0].external_id}
    response = client.get('/change_password', params = parameter)
    result = session.exec(
        select(EventTable, AttackTable, TargetProfileTable)
            .join(AttackTable, EventTable.parent_attack_id == AttackTable.id)
            .join(TargetProfileTable, AttackTable.target_id == TargetProfileTable.id)
            .order_by(EventTable.id.desc())
    ).first()

    # test database match
    assert result.TargetProfileTable.name == 'Jack Fishing',\
        "TargetProfileTable.name between database and test doesn't match"
    assert result.TargetProfileTable.email == 'jack.fishing@nowhere.westeros.org',\
        "TargetProfileTable.email between database and test doesn't match"
    assert result.AttackTable.external_id == 'test_change_password_html_page_1',\
        "AttackTable.external_id between database and test doesn't match"
    assert result.AttackTable.scheme_name == 'generic_org_change_password',\
        "AttackTable.scheme_name between database and test doesn't match"
    assert result.AttackTable.target.id == result.TargetProfileTable.id ,\
        "AttackTable.target.id between database and test doesn't match"
    assert result.EventTable.kind == 'Email.sent, Link.clicked',\
        "EventTable.kind between database and test doesn't match"
    assert result.EventTable.detail == {"ip": "testclient"},\
        "EventTable.detail between database and test doesn't match"
    assert response.status_code == 200

    parameter = {"k": attacks[1].external_id}
    with pytest.raises(ValueError):
        response = client.get('/change_password', params = parameter)


def test_change_password_api(session, client):
    attacks = [
        AttackTable(
            external_id = 'test_change_password_api_1',
            scheme_name = 'generic_org_change_password',
            target = TargetProfileTable(
                name = 'Jack Fishing',
                email = 'jack.fishing@nowhere.westeros.org',
            ),
        ),
        AttackTable(
            external_id = 'test_change_password_api_2',
            scheme_name = 'invalid_scheme',
            target = TargetProfileTable(
                name = 'John Fishing',
                email = 'John.Fishing@nowhere.westeros.org',
            ),
        ),
    ]
    session.add_all(attacks)
    session.flush()

    parameter_json = {'k': attacks[0].external_id, 'p': 'password'}
    response = client.post('/api/change_password', json = parameter_json)

    result = session.exec(
        select(EventTable, AttackTable, TargetProfileTable)
            .join(AttackTable, EventTable.parent_attack_id == AttackTable.id)
            .join(TargetProfileTable, AttackTable.target_id == TargetProfileTable.id)
            .order_by(EventTable.id.desc())
    ).first()

    # test database match
    assert result.TargetProfileTable.name == 'Jack Fishing',\
        "TargetProfileTable.name between database and test doesn't match"
    assert result.TargetProfileTable.email == 'jack.fishing@nowhere.westeros.org',\
        "TargetProfileTable.email between database and test doesn't match"
    assert result.AttackTable.external_id == 'test_change_password_api_1',\
        "AttackTable.external_id between database and test doesn't match"
    assert result.AttackTable.scheme_name == 'generic_org_change_password',\
        "AttackTable.scheme_name between database and test doesn't match"
    assert result.AttackTable.target.id == result.TargetProfileTable.id ,\
        "AttackTable.target.id between database and test doesn't match"
    assert result.EventTable.kind == "Email.sent, Link.clicked, Password.inserted",\
        "EventTable.kind between database and test doesn't match"
    assert result.EventTable.detail == {
        "ip": "testclient",
        "password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
    }, "EventTable.detail between database and test doesn't match"

    parameter_json2 = {'k': attacks[1].external_id, 'p': 'password'}
    with pytest.raises(ValueError):
        response = client.post('/api/change_password', json = parameter_json2)


def test_payroll_update(session, client):
    attacks = [
        AttackTable(
            external_id = 'test_hr_benefit_html_page_1',
            scheme_name = 'payroll_update',
            target = TargetProfileTable(
                name = 'Jack Fishing',
                email = 'jack.fishing@nowhere.westeros.org',
            ),
        ),
        AttackTable(
            external_id = 'test_hr_benefit_html_page_2',
            scheme_name = 'invalid_scheme',
            target = TargetProfileTable(
                name = 'John Fishing',
                email = 'John.Fishing@nowhere.westeros.org',
            ),
        ),
    ]
    session.add_all(attacks)
    session.flush()

    response = client.get('/payroll_update', params={"k": attacks[0].external_id})
    assert response.status_code == 200


def test_hr_html(session, client):
    attacks = [
        AttackTable(
            external_id = 'test_hr_benefit_html_page_1',
            scheme_name = 'hr_benefits_update_page',
            target = TargetProfileTable(
                name = 'Jack Fishing',
                email = 'jack.fishing@nowhere.westeros.org',
            ),
        ),
        AttackTable(
            external_id = 'test_hr_benefit_html_page_2',
            scheme_name = 'invalid_scheme',
            target = TargetProfileTable(
                name = 'John Fishing',
                email = 'John.Fishing@nowhere.westeros.org',
            ),
        ),
    ]

    session.add_all(attacks)
    session.flush()
    response = client.get('/internal/hr-portal', params={"k": attacks[0].external_id})
    assert response.status_code == 200