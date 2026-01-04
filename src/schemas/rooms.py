from pydantic import BaseModel,Field,ConfigDict



class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids:list[int] | None = None


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class Room_patchRequest(BaseModel):
    description: str | None = None
    title: str | None = None
    price: int | None = None
    quantity: int | None = None


class Room_patch(BaseModel):
    hotel_id: int| None = None
    description: str | None = None
    title: str | None = None
    price: int | None = None
    quantity: int | None = None