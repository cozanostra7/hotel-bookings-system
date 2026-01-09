from pydantic import EmailStr
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models import UsersOrm
from src.repositories.mappers.mappers import UserMapper
from src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserMapper

    async def get_user_with_hashed_password(
            self,
            email: EmailStr,
    ) -> UserWithHashedPassword | None:
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        if model is None:
            return None

        return UserWithHashedPassword.model_validate(model)