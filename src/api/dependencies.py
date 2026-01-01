from typing import Annotated
from fastapi import Depends, Query,HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from src.services.auth import AuthService


class Pagination_params(BaseModel):
    page: Annotated[int | None , Query(1, description='page', gt=0, lt=100)]
    per_page:Annotated[int | None , Query(None)]



PaginationDep = Annotated[Pagination_params,Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get('access_token', None)
    if not token:
        raise HTTPException(status_code=401,detail='You are not authorized')
    return token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().encode_token(token)
    return data['user_id']


UserIDDep = Annotated[int,Depends(get_current_user_id)]