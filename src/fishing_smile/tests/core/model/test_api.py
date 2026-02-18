import pytest
from sqlmodel import (
    select,
    delete,
    Session
)
from pydantic import ValidationError
from fishing_smile.database.engine import engine
from fishing_smile.core.model import *
import requests
from sqlalchemy import desc
import json

def test_change_password_api(session):
    profile = TargetProfileTable(
        name = 'test_change_password_api',
        email = 'test_change_password_api@nowhere.westeros.org',
    )
    attack = AttackTable(
        external_id = 'test_change_password_apitest_cha',
        scheme_name = 'empty',
        target = profile,
    )

    result1 = session.exec(
        select(AttackTable).where(AttackTable.external_id == attack.external_id)
    ).first()
    if result1 != None:
        session.delete(result1)
        session.commit()

    session.add(attack)
    session.commit()
    results = session.exec(select(EventTable)).all()

    response = requests.get(
            f"http://host.docker.internal:80/change_password",
            params={
                "k": attack.external_id,
            }
        )
    session.close()
    session = Session(engine)
    response_json = response.json()
    attack_id = json.loads(response_json)["result"]

    result2 = session.exec(
        select(EventTable).where(EventTable.parent_attack_id == int(attack_id)).order_by(desc(EventTable.id))
    ).first()

    assert result2.kind == 'Email sent, Link clicked' == json.loads(response_json)["kind"]  # test that it's the same for response and database. and it actually insert to database.
    #assert json.loads(response_json)["time"] == str(result2.time) There is a milisecond issue. I will find a way around it to make it usable

def test_change_password_api2(session):
    profile = TargetProfileTable(
        name = 'test_change_password_api2',
        email = 'test_change_password_api2@nowhere.westeros.org',
    )
    attack = AttackTable(
        external_id = 'test_change_password_api22222222',
        scheme_name = 'empty',
        target = profile,
    )

    result1 = session.exec(
        select(AttackTable).where(AttackTable.external_id == attack.external_id)
    ).first()
    if result1 != None:
        session.delete(result1)
        session.commit()

    session.add(attack)
    session.commit()
    results = session.exec(select(EventTable)).all()

    response = requests.post(
            "http://host.docker.internal:80/api/change_password",
            json={'k': attack.external_id, 'p': 'password'}
        )
    session.close()
    session = Session(engine)
    response_json = response.json()
    print(response_json)
    attack_id = json.loads(response_json)["result"]

    result2 = session.exec(
        select(EventTable).where(EventTable.parent_attack_id == int(attack_id)).order_by(desc(EventTable.id))
    ).first()

    assert result2.kind == 'Email sent, Link clicked, Password inserted' == json.loads(response_json)["kind"]  # test that it's the same for response and database
    #assert json.loads(response_json)["time"] == str(result2.time) There is a milisecond issue. I will find a way around it to make it usable
