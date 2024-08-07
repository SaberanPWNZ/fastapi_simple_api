import logging

from fastapi_cache.decorator import cache
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from auth.database import get_async_session, get_access_token_db
from items.models import Item
from items.schemas import ItemCreate, ItemResponse
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend

from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

from user.users_model import User, UserBase, AccessToken

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

authentication = APIRouter(prefix='/auth', tags=['auth'])
items_router = APIRouter(
    prefix="/items",
    tags=['Items']
)

fastapi_users = FastAPIUsers[User, User.id](
    get_user_manager,
    [auth_backend],
)

authentication.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

authentication.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"], )

current_user = fastapi_users.current_user()
current_user_token = fastapi_users.authenticator.current_user_token()


@items_router.post('/create')
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
                            })


@cache(expire=60)
@items_router.get('/', response_model=list[ItemResponse], dependencies=[Depends(current_user_token)])
async def get_all_items(session: AsyncSession = Depends(get_async_session),
                        ):
    try:
        query = select(Item).where(Item.title == 'string')
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail={'status': 'error', 'message': 'invalid token'})
