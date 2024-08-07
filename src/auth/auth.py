from fastapi import Depends
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from fastapi_users.authentication import BearerTransport
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy

from auth.database import get_access_token_db
from user.users_model import AccessToken
from fastapi.security import api_key

SECRET = "SECRET"

# api_key.APIKey()
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
