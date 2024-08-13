import os

from dotenv import load_dotenv

load_dotenv()


class DataBase:
    NAME: str = os.getenv('DB_NAME')
    PORT: int = os.getenv('DB_PORT')
    USER: str = os.getenv('DB_USERNAME')
    PASSWORD: str = os.getenv('DB_PASSWORD')
    HOST: str = os.getenv('DB_HOST')
    JWT_SECRET: str = os.getenv('JWT_SECRET_KEY')

    @staticmethod
    def DATABASE_URL():
        return f"postgresql+asyncpg://{DataBase.USER}:{DataBase.PASSWORD}@{DataBase.HOST}:{DataBase.PORT}/{DataBase.NAME}"

class DataBaseTest:
    NAME: str = os.getenv('DB_NAME_TEST')
    PORT: int = os.getenv('DB_PORT_TEST')
    USER: str = os.getenv('DB_USERNAME_TEST')
    PASSWORD: str = os.getenv('DB_PASSWORD_TEST')
    HOST: str = os.getenv('DB_HOST_TEST')
    JWT_SECRET: str = os.getenv('JWT_SECRET_KEY_TEST')

    @staticmethod
    def DATABASE_URL_TEST():
        return f"postgresql+asyncpg://{DataBaseTest.USER}:{DataBaseTest.PASSWORD}@{DataBaseTest.HOST}:{DataBaseTest.PORT}/{DataBaseTest.NAME}"
