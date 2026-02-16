import pytest
from sqlmodel import (
    Session,
    delete,
)

from fishing_smile.database.engine import engine
from fishing_smile.core.model import *


@pytest.fixture(name = 'session')
def empty_database_session():
    with Session(engine) as session:
        session.exec(delete(TargetProfileTable))
        session.exec(delete(AttackTable))
        yield session
        session.rollback()
