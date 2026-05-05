import json
from pathlib import Path
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_poll
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope='session', autouse=True)
async def check_test_mode():
    """Ensure tests only run in TEST mode"""
    assert settings.MODE == 'TEST', "Tests must run in TEST mode! Set MODE=TEST in .env"


@pytest.fixture(scope='session', autouse=True)
async def initialize_cache():
    FastAPICache.init(InMemoryBackend())
    yield


async def get_db_null_pool() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_poll) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    """Provide database manager for each test function"""
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope='session', autouse=True)
async def setup_database(check_test_mode):
    assert settings.MODE == 'TEST'
    
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


    data_path = Path('tests/')
    
    with (data_path / 'mock_hotels.json').open(encoding='utf-8') as f:
        hotels_data = json.load(f)
    
    with (data_path / 'mock_rooms.json').open(encoding='utf-8') as f:
        rooms_data = json.load(f)
    
    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels_data]
    rooms = [RoomAdd.model_validate(room) for room in rooms_data]
    
    async with DBManager(session_factory=async_session_maker_null_poll) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Provide async HTTP client for tests"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test'
    ) as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
async def register_user(ac: AsyncClient, setup_database):
    response = await ac.post(
        '/auth/register',
        json={
            'email': 'pes@kot.com',
            'password': '123456',
            'fullname': 'Test User'
        }
    )
    assert response.status_code == 200, f"User registration failed: {response.json()}"


@pytest.fixture(scope='session')
async def authenticated_ac(register_user,ac) -> AsyncGenerator[AsyncClient, None]:

    response = await ac.post(
        '/auth/login',
        json={
            'email': 'pes@kot.com',
            'password': '123456'
        }
    )
    assert ac.cookies['access_token']
    yield ac
