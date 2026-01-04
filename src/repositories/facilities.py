from src.models import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilitites import Facilities, RoomsFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities


class RoomsFacilityRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacility