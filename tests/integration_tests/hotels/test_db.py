from src.database import async_session_maker, async_session_maker_null_poll
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_info = HotelAdd(title='Silk Road',location='Samarkand')
    async with DBManager(session_factory=async_session_maker_null_poll) as db:
        new_hotel_data = await db.hotels.add(hotel_info)
        await db.commit()