from src.repositories.base import BaseRepository
from src.models import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm