from datetime import date

from src.schemas.facilitites import RoomsFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, Room_patchRequest, Room_patch
from fastapi import Query,Body,APIRouter
from src.api.dependencies import DBDep
from fastapi_cache.decorator import cache
router= APIRouter(prefix = '/hotels',tags=['Rooms'])

@router.get('/{hotel_id}/rooms')
@cache(expire=10)
async def get_all_rooms(hotel_id:int,
                        db:DBDep,
                        date_from: date = Query(example='2026-02-01'),
                        date_to: date = Query(example='2026-02-10')
                        ):

        return await db.rooms.get_filtered_by_time(hotel_id=hotel_id,date_from=date_from,date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
@cache(expire=10)
async def get_room(
        hotel_id:int,
        room_id:int,
        db:DBDep,

):
        return await db.rooms.get_room_with_facilities(id = room_id,hotel_id=hotel_id)


@router.post('/{hotel_id}/rooms')
async def create_room(db:DBDep,hotel_id:int,room_info:RoomAddRequest = Body
    (openapi_examples=
     {'1': {'summary': 'Rooms', 'value': {
         'title': 'Title of the hotel!',
         'description': 'Description of the hotel',
         'price':150,
         'quantity':2,
         'facilities_ids':[0],
     }}})
                      ):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_info.model_dump())
    room = await db.rooms.add(_room_data)
    rooms_facilities_data = [RoomsFacilityAdd(room_id=room.id,facility_id=f_id) for f_id in room_info.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}

@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
        db: DBDep,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: Room_patchRequest,
        db: DBDep,
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = Room_patch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data,partially_edited=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])
    await db.commit()
    return {"status": "OK"}

@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_hotel(hotel_id:int,room_id:int,db:DBDep):
    await db.rooms.delete(id=room_id,hotel_id=hotel_id)
    await db.commit()
    return {'status':'Ok'}