import pytest

from tests.test_base import TestRequest

check
@pytest.mark.parametrize("title, article, partner_price, rrp_price, EAN, category, status, warranty", [
    ('Планшет Intuos S Black', 'CTL-4100K-N', 3728, 4189, '4949268621335', 'tablets', 'in stock', 12),
('Планшет Intuos S Black', 'CTL-4100K-N', 3728, 4189, '4949268621335', 'tablets', 'in stock', 12),
('Планшет Intuos S Black', 'CTL-4100K-N', 3728, 4189, '4949268621335', 'tablets', 'in stock', 12)
                ])
@pytest.mark.asyncio
async def test_create_item(create_user, route_items, async_client,
                           title, article, partner_price, rrp_price, EAN, category, status, warranty):
    tester = TestRequest(url=route_items, async_client=async_client)
    token = create_user
    request = await tester.post(
        headers={'Access_token': token

                 },
        body={
            "title": title,
            "article": article,
            "partner_price": partner_price,
            "rrp_price": rrp_price,
            "EAN": EAN,
            "category": category,
            "status": status,
            "warranty": warranty,

        }

    )
    response = request.json()
    assert request.status_code == 201, f"Unexpected status code: {request.status_code}"
    assert response['status'] == 'success', f"Unexpected status: {response['status']}"
    assert response['items'] == title, f"Unexpected item: {response['items']}"

@pytest.mark.asyncio
async def test_get_all_items(create_user, create_item, route_all_items, async_client):
    tester = TestRequest(url=route_all_items, async_client=async_client)

    request = await tester.get(
        headers={'Access_token': create_user})

    pass
