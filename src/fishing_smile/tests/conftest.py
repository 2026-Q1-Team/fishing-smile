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
        session.exec(delete(EventTable))
        session.exec(delete(AttackTable))
        session.exec(delete(TargetProfileTable))
        yield session
        session.rollback()
