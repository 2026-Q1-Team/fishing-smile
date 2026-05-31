import pytest
from sqlmodel import (
    Session,
    delete,
)

from fishing_smile.database.engine import engine
from fishing_smile.core.model import *


# NOTE: Adapted from https://gist.github.com/kissgyorgy/e2365f25a213de44b9a2
# Depends on "obsecure" property of session begining inside an outer transaction
# which allows `session.commit()` called by test subjects to be later rolled back
# via the outer transaction.
#
# I said "obsecure" because I can't find explicit explanation of this behaviour
# in offical doc.
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
