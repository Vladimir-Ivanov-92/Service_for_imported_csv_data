import os

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import UserCreate, ShowUser
from db.dals import UserDAL, FileDAL
from db.models import File
from db.session import get_db

import pandas as pd


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


async def _load_data(file_path, db: AsyncSession = Depends(get_db)):
    df = pd.read_csv(file_path)
    table_name = os.path.splitext(os.path.basename(file_path))[0]

    async with db as session:
        async with session.begin():
            # await df.to_sql(table_name, con=session.connection(),
            #                 if_exists='append')

            # Правильный путь к файлу после перемещения в папку uploads
            file_name = os.path.basename(file_path)

            # Сохранение информации о колонках в таблице files
            columns = df.columns.tolist()
            file_name_to_db = file_name.split(".")[0]
            for column in columns:
                insert_query = File(file_name=file_name_to_db, columns=column)
                session.add(insert_query)

            await session.flush()

    return table_name


async def _get_tables(db: AsyncSession = Depends(get_db)):
    async with db as session:
        async with session.begin():
            file_dal = FileDAL(session)
            tables = await file_dal.get_tables()
    return tables
