from src.schemas.rooms import RoomAdd, RoomAddRequest, Room_patchRequest
from fastapi import Query,Body,APIRouter
from src.api.dependencies import DBDep
router= APIRouter(prefix = '/hotels',tags=['Rooms'])

@router.get('/{hotel_id}/rooms')
async def get_all_rooms(hotel_id:int,db:DBDep):

        return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id:int,room_id:int,db:DBDep):
        return await db.rooms.get_one_or_none(
            id = room_id,hotel_id=hotel_id)


@router.post('/{hotel_id}/rooms')
async def create_room(db:DBDep,hotel_id:int,room_info:RoomAddRequest = Body
    (openapi_examples=
     {'1': {'summary': 'Rooms', 'value': {
         'title': 'Title of the hotel!',
         'description': 'Description of the hotel',
         'price':150,
         'quantity':2
     }}})
                      ):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_info.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}

@router.patch('/{hotel_id}/rooms/{room_id}')
async def partially_edit_rooms(
        hotel_id:int,room_id:int,
        room_info:Room_patchRequest,
        db:DBDep):

    _room_data = Room_patchRequest(hotel_id=hotel_id, **room_info.model_dump())
    await db.rooms.edit(_room_data,partially_edited=True,id = room_id)
    await db.commit()
    return {'status':'Ok'}

@router.put('/{hotel_id}/rooms/{room_id}')
async def update_rooms(hotel_id:int,room_id:int,room_info:RoomAddRequest,db:DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_info.model_dump())
    await db.rooms.edit(_room_data,id = room_id)
    await db.commit()
    return {'status': 'Ok'}

@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_hotel(hotel_id:int,room_id:int,db:DBDep):
    await db.rooms.delete(id=room_id,hotel_id=hotel_id)
    await db.commit()
    return {'status':'Ok'}