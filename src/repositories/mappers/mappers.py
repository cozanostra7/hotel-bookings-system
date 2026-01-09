from src.models import HotelsOrm, BookingsOrm, UsersOrm, RoomsOrm, FacilitiesOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.facilitites import Facilities
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User


class HotelMapper(DataMapper):
    db_model = HotelsOrm
    schema=Hotel


class RoomMapper(DataMapper):
    db_model = RoomsOrm
    schema=Room


class RoomWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema=RoomWithRels

class UserMapper(DataMapper):
    db_model = UsersOrm
    schema=User

class BookingMapper(DataMapper):
    db_model = BookingsOrm
    schema=Booking


class FacilityMapper(DataMapper):
    db_model = FacilitiesOrm
    schema=Facilities