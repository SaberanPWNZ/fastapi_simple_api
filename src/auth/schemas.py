from typing import Optional

from fastapi_users import schemas, models
from pydantic import EmailStr


class UserRead(schemas.BaseModel):
    id: int
    email: str
    company_name: str

    class Config:
        model_config = {'from_attributes': True}

class UserCreate(schemas.BaseModel):
    email: EmailStr
    company_name: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:

        model_config = {'from_attributes': True}

class UserUpdate(schemas.BaseUserUpdate):
    class Config:

        model_config = {'from_attributes': True}
    pass
