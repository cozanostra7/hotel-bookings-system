from sqlalchemy import select,func

from src.repositories.base import BaseRepository
from src.models import BookingsOrm
from src.schemas.bookings import Booking

class RoomsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking
