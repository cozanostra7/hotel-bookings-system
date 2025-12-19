from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel


class Pagination_params(BaseModel):
    page: Annotated[int | None , Query(None, description='page', gt=0, lt=100)]
    per_page:Annotated[int | None , Query(None)]


PaginationDep = Annotated[Pagination_params,Depends()]