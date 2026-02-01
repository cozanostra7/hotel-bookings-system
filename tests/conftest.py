import json
from pathlib import Path

import pytest

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_poll, async_session_maker
from src.main import app
from src.models import *
from httpx import AsyncClient

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope='session',autouse=True)
async def check_test_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(scope='session',autouse=True)
async def setup_database(check_test_mode):
    assert settings.MODE == 'TEST'
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        data_path = Path('tests/')

        with (data_path / 'mock_hotels.json').open(encoding='utf-8') as f:
            hotels= json.load(f)

        with (data_path / 'mock_rooms.json').open(encoding='utf-8') as f:
            rooms = json.load(f)

        hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
        rooms = [RoomAdd.model_validate(room) for room in rooms]

        async with DBManager(session_factory=async_session_maker_null_poll) as db:
            db.hotels.add_bulk(hotels)
            db.rooms.add_bulk(rooms)
            await db.commit()


@pytest.fixture(scope='session',autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app,base_url='http://test') as ac:
        await ac.post(
            '/auth/register',
                    json={
                     'email':'pes@kot.com',
                     'password':'123456',
                     'fullname': 'Test User'})