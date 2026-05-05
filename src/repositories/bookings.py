from datetime import date

from sqlalchemy import select,func

from repositories.utils import rooms_ids_for_bookings
from schemas.bookings import BookingAdd
from src.repositories.base import BaseRepository
from src.models import BookingsOrm
from src.repositories.mappers.mappers import BookingMapper

class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingMapper


    async def get_bookings_with_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]


    async def add_bookings(self,data:BookingAdd,hotel_id:int):
        rooms_ids_to_get = rooms_ids_for_bookings(
             data.date_from, 
             data.date_to, 
             hotel_id=hotel_id)
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book:list[int] = rooms_ids_to_book_res.scalars().all()

        if data.room_id in rooms_ids_to_book:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise Exception