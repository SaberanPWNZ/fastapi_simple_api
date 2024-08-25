import os
import sys

from sqlalchemy import NullPool, create_engine, StaticPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from auth.db_helper import test_settings

TEST_DATABASE_URL = test_settings.DB_URL

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

test_engine = create_async_engine(TEST_DATABASE_URL)

session_maker_testdb = async_sessionmaker(
    expire_on_commit=False, bind=test_engine, autoflush=False
)

