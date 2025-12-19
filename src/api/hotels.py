from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel,Hotel_patch
from typing import Annotated
from fastapi import FastAPI,Query,Body,APIRouter,Depends


router= APIRouter(prefix = '/hotels',tags=['Hotels'])

hotels = [
    {'id':1,'title':'London','name':'London'},
    {'id':2,'title':'Barcelona','name':'Barcelona'},
    {'id':3,'title':'Tashkent','name':'Tashkent'},
    {'id':4,'title':'Samarkand','name':'Samarkand'},
    {'id':5,'title':'Berlin','name':'Berlin'},
    {'id':6,'title':'Tbilisi','name':'Tbilisi'},
    {'id':7,'title':'Athens','name':'Athens'},
]



@router.get('')
def read_hotels(
        pagination:PaginationDep,
        id: int | None = Query(None, description="Hotel ID"),
        title: str | None = Query(None, description="Hotel title")):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id']!=id:
            continue
        if title and hotel['title']!= title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page*(pagination.page-1):][:pagination.per_page]
    #return [hotel for hotel in hotels if hotel['title']==title and hotel['id'] == id]


@router.post('')
def create_hotels(hotel_info:Hotel = Body
    (openapi_examples=
     {'1':{'summary':'London','value':{
    'title':'Your hotel in the capital!',
    'name':'London Capitals'
}}})):
    global hotels
    hotels.append({
        'id':hotels[-1]['id'] + 1,
        'title':hotel_info.title
    })
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