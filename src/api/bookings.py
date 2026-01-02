from src.schemas.bookings import BookingAdd,BookingAddRequest
from fastapi import APIRouter
from src.api.dependencies import DBDep, UserIDDep

router= APIRouter(prefix = '/bookings',tags=['bookings'])

@router.post('')
async def add_bookings(
        room_id:int,
        user_id:UserIDDep,
        db:DBDep,
        booking_info:BookingAddRequest):
        room = await db.rooms.get_one_or_none(id=booking_info.room_id)
        room_price:int=room.price
        _booking_info = BookingAdd(
                user_id=user_id,
                price = room_price,
                **booking_info.model_dump()
        )



        booking = await db.bookings.add(_booking_info)
        await db.commit()
        return {'status':'Ok','data':booking}
