from fastapi import HTTPException
from fastapi import APIRouter
from starlette.responses import Response
from src.api.dependencies import UserIDDep, DBDep
from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd


from src.services.auth import AuthService

router = APIRouter(prefix="/auth",tags=["Authentication and Authorization"])

@router.post('/register')
async def register_user(data: UserRequestAdd,db:DBDep):
    hashed_password=AuthService().hash_password(data.password)
    new_user_data = UserAdd(fullname=data.fullname,email=data.email,hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit()
    return {'status': 'Ok'}



@router.post('/login')
async def login_user(data: UserRequestAdd,response:Response,db:DBDep):
        user = await db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401,detail='User with this email not found')

        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401,detail='invalid password')
        access_token = AuthService().create_access_token({'user_id':user.id})
        response.set_cookie('access_token',access_token)
        return {'access_token':access_token}


@router.get('/me')
async def me(user_id:UserIDDep,db:DBDep):

    user = await db.users.get_one_or_none(id=user_id)
    return user

@router.post('/logout')
async def logout_user(user_id:UserIDDep,response:Response):
    response.delete_cookie('access_token')
    return {'status': 'Ok'}