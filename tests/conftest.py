import asyncio
import base64
import json
import os
import databases
import httpx
import pytest
from alembic import command
from alembic.config import Config
from starlette.config import environ
from starlette.testclient import TestClient

from frontend_service import models, settings
from frontend_service.models import init_tables
from frontend_service.views import app
from orm.test_utils import *


@pytest.fixture
def client():
    return httpx.AsyncClient(app=app, base_url="http://test_server")
    # return httpx.Client(app=app,base_url="http://test_server")
    # return TestClient(app, raise_server_exceptions=True)

@pytest.fixture(scope="session")
def metadata(database):
    metadata = init_tables(database)
    return metadata

@pytest.fixture(scope="session")
def database():
    return databases.Database(str(settings.DATABASE_URL))


@pytest.fixture
def engine():
    return sqlalchemy.create_engine(str(settings.DATABASE_URL))

@pytest.fixture(autouse=True, scope="session")
def create_test_database(metadata, monkeysession):
    engine = sqlalchemy.create_engine(str(settings.DATABASE_URL))
    metadata.create_all(engine)
    # config = Config("alembic.ini")   # Run the migrations.
    # command.upgrade(config, "head")
    yield
    # command.downgrade(config, "head")                  # Run the tests.
    metadata.drop_all(engine)


@pytest.fixture(scope="session")
def monkeysession(request):
    from _pytest.monkeypatch import MonkeyPatch

    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture
def create_future():
    def _create_future(value):
        dd = asyncio.Future()
        dd.set_result(value)
        return dd

    return _create_future
