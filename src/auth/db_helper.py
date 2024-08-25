import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


# class DataBase:
#     NAME: str = os.getenv("DB_NAME")
#     PORT: int = os.getenv("DB_PORT")
#     USER: str = os.getenv("DB_USERNAME")
#     PASSWORD: str = os.getenv("DB_PASSWORD")
#     HOST: str = os.getenv("DB_HOST")
#     JWT_SECRET: str = os.getenv("JWT_SECRET_KEY")
#
#     @staticmethod
#     def DATABASE_URL():
#         return f"postgresql+asyncpg://{DataBase.USER}:{DataBase.PASSWORD}@{DataBase.HOST}:{DataBase.PORT}/{DataBase.NAME}"


# class DataBaseTest:
#     NAME: str = os.getenv("DB_NAME_TEST")
#     PORT: int = os.getenv("DB_PORT_TEST")
#     USER: str = os.getenv("DB_USERNAME_TEST")
#     PASSWORD: str = os.getenv("DB_PASSWORD_TEST")
#     HOST: str = os.getenv("DB_HOST_TEST")
#
#     @staticmethod
#     def DATABASE_URL_TEST():
#         return f"postgresql+asyncpg://{DataBaseTest.USER}:{DataBaseTest.PASSWORD}@{DataBaseTest.HOST}:{DataBaseTest.PORT}/{DataBaseTest.NAME}"


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class TestSettings(BaseSettings):
    DB_USER_TEST: str
    DB_PASS_TEST: str
    DB_HOST_TEST: str
    DB_NAME_TEST: str
    DB_PORT_TEST: int

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
test_settings = TestSettings()
