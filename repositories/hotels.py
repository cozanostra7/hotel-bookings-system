from repositories.base import BaseRepository
from src.models import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm
