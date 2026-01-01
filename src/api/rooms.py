from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, Room_patch, Room, RoomAddRequest, Room_patchRequest
from fastapi import Query,Body,APIRouter
from src.repositories.rooms import RoomsRepository

router= APIRouter(prefix = '/hotels',tags=['Rooms'])

@router.get('/{hotel_id}/rooms')
async def get_all_rooms(hotel_id:int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id:int,room_id:int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            id = room_id,hotel_id=hotel_id)


@router.post('/{hotel_id}/rooms')
async def create_room(hotel_id:int,room_info:RoomAddRequest = Body
    (openapi_examples=
     {'1': {'summary': 'Rooms', 'value': {
         'title': 'Title of the hotel!',
         'description': 'Description of the hotel',
         'price':150,
         'quantity':2
     }}})
                      ):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_info.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

    return {"status": "OK", "data": room}

@router.patch('/{hotel_id}/rooms/{room_id}')
async def partially_edit_rooms(
        hotel_id:int,room_id:int,
        room_info:Room_patchRequest):

    _room_data = Room_patchRequest(hotel_id=hotel_id, **room_info.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data,partially_edited=True,id = room_id)
        await session.commit()
    return {'status':'Ok'}

@router.put('/{hotel_id}/rooms/{room_id}')
async def update_rooms(hotel_id:int,room_id:int,room_info:RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_info.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data,id = room_id)
        await session.commit()
    return {'status': 'Ok'}

@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_hotel(hotel_id:int,room_id:int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id,hotel_id=hotel_id)
        await session.commit()
    return {'status':'Ok'}