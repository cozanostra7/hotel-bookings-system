from datetime import date

from pydantic import BaseModel,Field,ConfigDict


class BookingAddRequest(BaseModel):
    date_from : date
    date_to : date
    room_id:int



class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from : date
    date_to : date
    price:int



class Booking(BookingAdd):
    id:int

    model_config = ConfigDict(from_attributes=True)

# class Booking_patchRequest(BaseModel):
#     date_from : date
#     date_to : date
#
#
# class Booking_patch(BaseModel):
#     user_id: int| None = None
#     room_id: int| None = None
#     price: int | None = None
#     date_from : date
#     date_to : date