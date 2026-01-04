from src.models import FacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilitites import Facilities


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities