from sqlalchemy.engine import URL
from sqlmodel import create_engine

from fishing_smile.settings import get_settings


engine = create_engine(URL.create(
    **get_settings().db.model_dump()
))
