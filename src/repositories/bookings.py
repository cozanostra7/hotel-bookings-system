from sqlalchemy import select,func

from src.repositories.base import BaseRepository
from src.models import BookingsOrm
from src.repositories.mappers.mappers import BookingMapper

class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingMapper
