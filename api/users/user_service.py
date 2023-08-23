from api.users.user_models import UserCreate, ShowUser
from sqlalchemy.ext.asyncio import AsyncSession
from db.dals import UserDAL
from fastapi import Depends

from db.session import get_db


async def _create_new_user(body: UserCreate,
                           db: AsyncSession = Depends(get_db)) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                login=body.login,
                email=body.email
            )
            return ShowUser(
                user_id=user.user_id,
                login=user.login,
                email=user.email,
                is_active=user.is_active
            )
