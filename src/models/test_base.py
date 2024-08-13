from httpx import AsyncClient

from tests.conftest import async_session_maker, async_client


class TestRequest:
    def __init__(self, url, async_client):
        self.test_url = url
        self.async_client = async_client

    async def get(self, async_client: AsyncClient):
        async with async_session_maker() as session:
            session.execute()
            request = await async_client.get(url=self.test_url)
            return request.json()

    async def post(self, body: dict):
        async with async_session_maker() as session:
            request = await self.async_client.post(
                url=self.test_url,
                json=body
            )
            await session.commit()
            return request

    def get_user_data(self, email, company_name, is_active, is_superuser, is_verified):
        return {
            "email": email,
            "company_name": company_name,
            "is_active": is_active,
            "is_superuser": is_superuser,
            "is_verified": is_verified,
        }
