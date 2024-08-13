import asyncio
import os
import sys
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.items.models import ItemBase, Item
from src.models.users_model import UserBase, User, AccessToken
from src.auth.database import get_async_session
from src.auth.db_helper import DataBaseTest
from src.main import app
from tests.Locators import TestingRoute, BaseLocator, UserCreateLocator

TEST_DATABASE_URL = DataBaseTest.DATABASE_URL_TEST()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session



@pytest_asyncio.fixture(scope='function', autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(UserBase.metadata.create_all)
        await conn.run_sync(ItemBase.metadata.create_all)
        yield
    async with test_engine.begin() as conn:
        await conn.run_sync(lambda connection: connection.execute(User.__table__.delete()))
        await conn.run_sync(lambda connection: connection.execute(Item.__table__.delete()))
        await conn.run_sync(lambda connection: connection.execute(AccessToken.__table__.delete()))


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://127.0.0.1:8000/') as ac:
        yield ac

@pytest.fixture()
def route_client() -> str:
    url = TestingRoute(base_url=BaseLocator.base_url, test_url=UserCreateLocator.test_url)
    return url.get_absolute_url()
