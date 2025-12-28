from pydantic import BaseModel, Field,ConfigDict


class HotelAdd(BaseModel):
    title:str
    location:str


class Hotel(HotelAdd):
    id:int

    model_config = ConfigDict(from_attributes=True)


class Hotel_patch(BaseModel):
    title: str | None = Field(None),
    location: str | None = Field(None)



