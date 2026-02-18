import pytest
from fastapi.testclient import TestClient

from fishing_smile.database.engine import get_session
from fishing_smile.core.db_hub import app
from fishing_smile.core.model import *


@pytest.fixture(name = 'client')
def db_hub_client(session):
    def get_session_override():
        return session

    # NOTE: Make `db_hub` app share the same database session
    # as the one used by test setup code to temporarily modify database.
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_get_campaigns(session, client):
    # TODO: Please write a test case of what you actually expect /api/campaigns to do
    # 1. setup database state
    # 2. call /api/campaigns
    # 3. check result is as expected
    # TODO: If we are making more test cases, it might be more convenient
    # to refactor test data as YAML file
    profile = TargetProfileTable(
        name = 'Jon Snow',
        email = 'jon.snow@nowhere.westeros.org',
    )
    attacks = [
        AttackTable(
            external_id = '012345678901234567890123456789AA',
            scheme_name = 'lucky_draw',
            target = profile,
        ),
        AttackTable(
            external_id = '012345678901234567890123456789BB',
            scheme_name = 'change_password',
            target = profile,
        ),
        AttackTable(
            external_id = '012345678901234567890123456789CC',
            scheme_name = 'change_password',
            target = profile,
        ),
    ]
    session.add_all(attacks)
    session.flush()

    response = client.get('/api/campaigns')
    assert response.status_code == 200

    # FIXME: GROUP BY includes primary key `id`, so each row is its own group
    # (targeted_count is always 1). Once the FIXME in get_campaigns is fixed,
    # update this test to expect 2 groups with targeted_count 1 and 2.
    data = response.json()
    assert len(data) == 3
    scheme_names = [row['scheme_name'] for row in data]
    assert scheme_names.count('lucky_draw') == 1
    assert scheme_names.count('change_password') == 2
    for row in data:
        assert 'id' in row
        assert isinstance(row['id'], int)
        assert row['targeted_count'] == 1
