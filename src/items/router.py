import logging

from fastapi_cache.decorator import cache
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from auth.auth import get_api_key
from auth.database import get_async_session
from items.docs import ItemRouterDocs
from items.models import Item
from items.schemas import ItemCreate, ItemResponse, ItemUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

items_router = APIRouter(
    prefix="/items",
    tags=['Items'],
    dependencies=[Depends(get_api_key)]
)

#include_in_schema=False
@items_router.post('/create', status_code=201)
async def create_item(object: ItemCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Item).values(**object.dict())
        result = await session.execute(stmt)
        await session.commit()
        logger.info(f"Item inserted: {result}")
        return {'status': 'success', 'items': object.dict().get('title')}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail={
                                'status': 'error',
                                'detail': str(e)
                            })


@items_router.post('/update/{item_article}', status_code=200, summary=ItemRouterDocs.item_update_docs,
                   description=ItemRouterDocs.item_update_message_format)
async def update_item(item_article: str, item: ItemUpdate, session: AsyncSession = Depends(get_async_session)):
    query = select(Item).where(Item.article == item_article.upper())
    result = await session.execute(query)
    item_to_update = result.scalars().first()

    if not item_to_update:
        raise HTTPException(status_code=404,
                            detail={"status": 'error', "message": f'Item with article {item_article} not found'})
    updated_fields = {}

    for key, value in item.dict(exclude_unset=True).items():
        if getattr(item_to_update, key) != value:
            updated_fields[key] = value
            setattr(item_to_update, key, value)

    await session.commit()
    logger.info(f"Item updated: {item_to_update}")

    return {
        'status': 'success',
        'item': item_to_update.article,
        'updated_fields': updated_fields
    }
@cache(expire=60)
@items_router.get('/', status_code=200, response_model=list[ItemResponse], summary="get all items")
async def get_all_items(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Item)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail={'status': 'error', 'message': 'invalid token'})
