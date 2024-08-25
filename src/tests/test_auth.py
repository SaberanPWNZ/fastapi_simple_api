import httpx
import pytest

from tests.test_base import TestRequest
from tests.test_data import email_symbols_45, email_symbols_46


@pytest.mark.parametrize(
    "email, company_name, is_active, is_superuser, is_verified",
    [
        ("auchan_user1ssas92n66a22@auchan.com", "TEST Company", True, False, False),
        # ('moyo_user@moyo.com', "Moyo Company", True, False, False),
        # ('rozetka_user@Rozetka.com', "Rozetka", True, False, False),
        # (email_symbols_45, "Moyo Company", False, False, False)  #max lenght email = 45
    ],)
async def test_create_user_positive(
    # email,
    # company_name,
    # is_active,
    # is_superuser,
    # is_verified,
    route_client,
    async_client: httpx.AsyncClient,

):
    # tester = TestRequest(url=route_client)
    # data = tester.get_user_data(
    # email, company_name, is_active, is_superuser, is_verified    #)
    data = {
        "email": "moyo_user@moyo.com",
        "company_name": "Moyo Company",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    }
    response = await async_client.post(url="http://127.0.0.1:8000/auth", json=data)
    assert response.status_code == 201
    assert len(response.json()["api_token"]) == 43


@pytest.mark.parametrize('email, company_name, is_active, is_superuser, is_verified', [
    ('auchan_userauchan.com', "TEST Company", False, False, False),
    ('moyo_usermoyo.com', "Moyo Company", False, False, False),
    ('rozetka_user_Rozetka.com', "Rozetka", False, False, False),
    ('rozetka_user_Rozetka.com', "False", 'text', 123, 'False'),
    (True, False, 'text', 123, 'False'),
    ('rozetka_user_Rozetka.com', "False", 'text', 123, 'False'),
    (email_symbols_46, "Moyo Company", False, False, False)  #test 46 symbols on email = error
])
@pytest.mark.asyncio
async def test_create_user_negative(email, company_name, is_active, is_superuser, is_verified, async_client,
                                    route_client):
    tester = TestRequest(url=route_client, async_client=async_client)
    data = tester.get_user_data(email, company_name, is_active, is_superuser, is_verified)
    response = await tester.post(body=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_api_key():
    pass
