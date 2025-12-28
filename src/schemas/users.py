from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRequestAdd(BaseModel):
    email:EmailStr
    password:str
    fullname:str | None = Field(None)


class  UserAdd(BaseModel):
    email:EmailStr
    hashed_password:str
    fullname: str


class User(UserAdd):
    id:int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
