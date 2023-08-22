from pydantic import EmailStr
from sqlalchemy import select

from db.models import User, FileStructure


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


class FileStructureDAL:

    def __init__(self, db_session):
        self.db_session = db_session

    async def get_tables(self) -> dict[str]:
        tables = {}

        query = select(FileStructure.file_name, FileStructure.columns)
        result = await self.db_session.execute(query)
        result_raw = result.fetchall()
        for row in result_raw:
            file_name = row[0]
            columns = row[1].split(',')
            if file_name not in tables:
                tables[file_name] = columns
            else:
                tables[file_name].extend(columns)

        return tables
