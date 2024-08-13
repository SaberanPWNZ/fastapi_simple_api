from fastapi_users import schemas


class AccessTokenRead(schemas.BaseModel):
    api_token: str
    user_id: int
    id: int
    class ConfigDict:
        from_attributes = True
