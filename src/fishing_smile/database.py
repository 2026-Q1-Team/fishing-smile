import logging
_logger = logging.getLogger(__name__)
from sqlalchemy.engine import URL
from sqlmodel import (
    SQLModel,
    create_engine,
)

from fishing_smile.settings import get_settings
from fishing_smile.core.model import *


engine = create_engine(URL.create(
    **get_settings().db.model_dump()
))


def initialize_database():
    _logger.info('initializing database')
    SQLModel.metadata.create_all(engine)

