from datetime import datetime, timezone
from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter

from src.auth.api_key import generate_api_key, default_expiry_date
from src.auth.database import get_async_session
from src.auth.schemas import UserCreate
from src.models.schemas import AccessTokenRead
from src.models.users_model import User, AccessToken

auth_router = APIRouter(prefix='/auth')
api_key_header = APIKeyHeader(name='Access_token', auto_error=False)


async def get_api_key(
        session: AsyncSession = Depends(get_async_session),
        api_key_header: str = Security(api_key_header),
) -> object:
    stmt = select(AccessToken).where(AccessToken.api_token == api_key_header)
    result = await session.execute(stmt)
    tokens = result.scalars().all()
    if tokens:
        return api_key_header
    else:
        raise HTTPException(
            status_code=403, detail="Could not validate credentials"

        )


@auth_router.post('', response_model=AccessTokenRead, status_code=201)
async def user_register(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        existing_user = await session.execute(
            select(User).filter(User.email == user.email)
        )
        if existing_user.scalars().first():
            raise HTTPException(
                status_code=400,
                detail={'status': 'error', 'message': 'This email already exists'}
            )

        new_user = User(**user.model_dump())
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        key = generate_api_key()
        api_token = AccessToken(
            user_id=new_user.id,
            api_token=key,
            created_at=datetime.now(timezone.utc),
            expired_at=default_expiry_date()
        )
        session.add(api_token)
        await session.commit()

        token_data = {
            "id": api_token.id,
            "user_id": api_token.user_id,
            "api_token": api_token.api_token,
            "created_at": api_token.created_at,
            "expired_at": api_token.expired_at
        }

        return AccessTokenRead(**token_data)

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail={'status': 'error', 'message': 'bad request'}
        )
