from typing import AsyncGenerator
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

import auth.auth
from auth.database import get_async_session

from src.items.models import ItemBase, Item
from src.models.users_model import UserBase, User, AccessToken

from src.main import app, auth_router
from tests.Locators import (
    TestingRoute,
    BaseLocator,
    UserCreateLocator,
    ItemCreateLocator,
    ItemGetLocator,
)
from tests.test_base import TestRequest
from tests.tests import session_maker_testdb, test_engine



async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    print("Using test database session")
    async with session_maker_testdb().begin() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_db
@pytest_asyncio.fixture(autouse=True, scope="function")
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(UserBase.metadata.create_all)
        await conn.run_sync(ItemBase.metadata.create_all)
        yield
    async with test_engine.begin() as conn:
        await conn.run_sync(lambda connection: connection.execute(User.__table__.delete()))
        await conn.run_sync(lambda connection: connection.execute(Item.__table__.delete()))
        await conn.run_sync(lambda connection: connection.execute(AccessToken.__table__.delete()))


@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncClient:
    transport_api = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport_api, base_url="http://127.0.0.1:8000/"
    ) as client:

        yield client


@pytest.fixture
def route_client() -> str:
    url = TestingRoute(
        base_url=BaseLocator.base_url, test_url=UserCreateLocator.test_url
    )
    return url.get_absolute_url()


@pytest.fixture
def route_items() -> str:
    url = TestingRoute(
        base_url=BaseLocator.base_url, test_url=ItemCreateLocator.test_url
    )
    return url.get_absolute_url()


def route_all_items() -> str:
    url = TestingRoute(base_url=BaseLocator.base_url, test_url=ItemGetLocator.test_url)
    return url.get_absolute_url()


@pytest_asyncio.fixture
async def create_user(route_client, async_client):
    tester = TestRequest(url=route_client, async_client=async_client)
    data = tester.get_user_data(
        "test_user1@gmail.com", "test_company", "True", "False", "True"
    )

    response = await tester.post(body=data)
    if response.status_code == 422:
        raise ValueError("Failed to create user: Unprocessable Entity")

    token = response.json().get("api_token")
    if token is None:
        raise ValueError("Failed to obtain token")

    return token
