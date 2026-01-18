from datetime import date

from sqlalchemy import select,func

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
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all]
