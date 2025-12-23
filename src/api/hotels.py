from sqlalchemy.orm import sessionmaker

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models import HotelsOrm
from src.schemas.hotels import Hotel,Hotel_patch
from typing import Annotated
from fastapi import FastAPI,Query,Body,APIRouter,Depends
from sqlalchemy import insert,select,func
from repositories.hotels import HotelsRepository


router= APIRouter(prefix = '/hotels',tags=['Hotels'])



@router.get('')
async def read_hotels(
        pagination:PaginationDep,
        location: str | None = Query(None, description="location of the hotel"),
        title: str | None = Query(None, description="Hotel title"),):

    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
       return await HotelsRepository(session).get_all(
           location = location,
           title = title,
           limit=per_page,
           offset=per_page * (pagination.page - 1))




@router.post('')
async def create_hotels(hotel_info:Hotel = Body
    (openapi_examples=
     {'1':{'summary':'London','value':{
    'title':'Your hotel in the capital!',
    'location':'London Capitals'
}}})):
    async with async_session_maker() as session:
        add_hotel_stmt = insert (HotelsOrm).values(**hotel_info.model_dump())
        print(add_hotel_stmt.compile(engine,compile_kwargs={'literal_binds':True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {'status': 'Ok'}

@router.patch('/{hotel_id}')
def edit_hotel(hotel_id:int,
               hotel_info:Hotel_patch):

    global hotels
    hotel = [hotel for hotel in hotels if hotel['id']==hotel_id][0]
    if hotel_info.title:
        hotel['title']=hotel_info.title
    if hotel_info.name:
        hotel['name']=hotel_info.name
    return {'status':'Ok'}
@router.put('/{hotel_id}')
def update_hotels(hotel_id:int,hotel_info:Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id']== hotel_id][0]
    hotel['title'] = hotel_info.title
    hotel['name'] = hotel_info.name
    return {'status': 'Ok'}

@router.delete('/{hotel_id}')
def delete_hotel(hotel_id:int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id']!=hotel_id]
    return {'status':'Ok'}