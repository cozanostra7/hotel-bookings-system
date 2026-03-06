from src.database import async_session_maker, async_session_maker_null_poll
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_add_hotel(db):
    hotel_info = HotelAdd(title='Silk Road',location='Samarkand')

    new_hotel_data = await db.hotels.add(hotel_info)
    await db.commit()