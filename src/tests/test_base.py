from httpx import AsyncClient
from tests.tests import session_maker_testdb


class TestRequest:
    def __init__(self, url=None, async_client: AsyncClient = None):
        self.test_url = url
        self.async_client = async_client

    async def get(self, headers=None):
        async with session_maker_testdb() as session:
            request = await self.async_client.get(url=self.test_url, headers=headers)
            session.commit()
            return request.json()

    async def post(self, body: dict, headers=None):
        async with session_maker_testdb() as session:
            request = await self.async_client.post(
                url=self.test_url,
                json=body,
                headers=headers
            )
            await session.commit()
            return request

    @staticmethod
    def get_user_data(email, company_name, is_active, is_superuser, is_verified):
        return {
            "email": email,
            "company_name": company_name,
            "is_active": is_active,
            "is_superuser": is_superuser,
            "is_verified": is_verified,
        }

    def get_item_data(self, title, article, partner_price, rrp_price, EAN, category, status, warranty):
        return {
            "title": title,
            "article": article,
            "partner_price": partner_price,
            "rrp_price": rrp_price,
            "EAN": EAN,
            "category": category,
            "status": status,
            "warranty": warranty,
        }
