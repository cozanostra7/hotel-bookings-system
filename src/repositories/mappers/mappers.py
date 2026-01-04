from src.models import HotelsOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotel


class HotelMapper(DataMapper):
    db_model = HotelsOrm
    schema=Hotel