import pytest
from sqlmodel import (
    select,
)
from fastapi.testclient import TestClient
from argon2 import PasswordHasher

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

