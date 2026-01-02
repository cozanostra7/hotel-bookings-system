from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import Hotel_patch, HotelAdd
from fastapi import Query,Body,APIRouter


router= APIRouter(prefix = '/hotels',tags=['Hotels'])



@router.get('')
async def read_hotels(
        pagination:PaginationDep,
        db:DBDep,
        location: str | None = Query(None, description="location of the hotel"),
        title: str | None = Query(None, description="Hotel title"),):

    per_page = pagination.per_page or 5

    return await db.hotels.get_all(
        location = location,
        title = title,
        limit=per_page,
        offset=per_page * (pagination.page - 1))



@router.get("/{hotel_id}")
async def get_hotel(hotel_id:int,db:DBDep):
        return await db.hotels.get_one_or_none(
            id = hotel_id)


@router.post('')
async def create_hotels(db:DBDep,hotel_info:HotelAdd = Body
    (openapi_examples=
     {'1':{'summary':'London','value':{
    'title':'Your hotel in the capital!',
    'location':'London Capitals'
}}})):

        hotel = await db.hotels.add(hotel_info)
        await db.commit()
        return {'status': 'Ok',"data":hotel}

@router.patch('/{hotel_id}')
async def edit_hotel(hotel_id:int,
               hotel_info:Hotel_patch,db:DBDep):

        await db.hotels.edit(hotel_info,partially_edited=True,id = hotel_id)
        await db.commit()
        return {'status':'Ok'}
@router.put('/{hotel_id}')
async def update_hotels(hotel_id:int,hotel_info:HotelAdd,db:DBDep,):
        await db.hotels.edit(hotel_info,id = hotel_id)
        await db.commit()
        return {'status': 'Ok'}

@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id:int,db:DBDep):
        await db.hotels.delete(id=hotel_id)
        await db.commit()
        return {'status':'Ok'}