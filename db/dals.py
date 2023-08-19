from pydantic import EmailStr

from db.models import User


# TODO: использовать библиотеку fastapi-users вместо самостоятельного создания User
class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session):
        self.db_session = db_session

    # TODO: добавить проверку сущестования пользователья в БД перед созданием
    async def create_user(self, login: str, email: EmailStr) -> User:
        # create new user
        new_user = User(login=login, email=email)
        # add new user
        self.db_session.add(new_user)
        # async synchronize session data with database
        await self.db_session.flush()
        return new_user
