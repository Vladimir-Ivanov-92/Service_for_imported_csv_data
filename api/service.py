import os
from typing import Iterable

from fastapi import Depends
from pandas import DataFrame
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import UserCreate, ShowUser
from db.dals import UserDAL, FileStructureDAL
from db.models import FileStructure
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
                insert_query = FileStructure(file_name=file_name_to_db, columns=column)
                session.add(insert_query)

            await session.flush()

    return table_name


async def _get_tables(db: AsyncSession = Depends(get_db)):
    async with db as session:
        async with session.begin():
            file_dal = FileStructureDAL(session)
            tables = await file_dal.get_tables()
    return tables


async def _get_name_columns_from_csv_table(table: DataFrame,
                               db: AsyncSession = Depends(get_db)) -> DataFrame:
    async with db as session:
        async with session.begin():
            # Получение имен столбцов таблицы:
            name_columns = table.columns
    return name_columns
async def _get_columns_data_from_csv_table(table: DataFrame,
                               db: AsyncSession = Depends(get_db)) -> Iterable:
    async with db as session:
        async with session.begin():
            # Получение имен столбцов таблицы:
            columns_data = table.iterrows()
    return columns_data