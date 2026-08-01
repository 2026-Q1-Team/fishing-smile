import pytest
from sqlmodel import (
    Session,
    delete,
)

from fishing_smile.database.engine import engine
from fishing_smile.core.model import *


@pytest.fixture(name = 'session')
def empty_database_session():
    connection = engine.connect()
    transaction = connection.begin()
    with Session(bind = connection, join_transaction_mode = 'create_savepoint') as session:
        session.exec(delete(EventTable))
        session.exec(delete(AttackTable))
        session.exec(delete(TargetProfileTable))
        yield session
    transaction.rollback()
    connection.close()
