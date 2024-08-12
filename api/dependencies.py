import logging
from typing import Annotated, Any

from fastapi import Depends
from api.settings import Settings

from ait.core.db import InfluxDBBackend

# from sqlmodel import Session, create_engine


logger = logging.getLogger(__name__)

# Settings from .env files and environment variables
settings = Settings()

# SQL connections
# engine = create_engine(settings.DB_URL, echo=settings.DB_ECHO)


# def get_session():
#     with Session(engine) as session:
#         yield session


# get_session_manager = contextlib.contextmanager(get_session)


# SessionDep = Annotated[Session, Depends(get_session)]


def get_client():
    backend = InfluxDBBackend()
    backend.connect()
    return backend


InfluxClient = Annotated[Any, Depends(get_client)]
