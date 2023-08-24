import os

import pandas as pd
from fastapi import Depends, File, Query, UploadFile
from pandas import DataFrame
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals import FileStructureDAL
from db.session import get_db


def _load_csv_to_uploads(file: UploadFile = File(...)) -> str:
    file_path = f"uploads/{file.filename}"
    with open(file_path, 'wb') as f:
        f.write(file.file.read())
    return file_path


async def _load_data_from_csv_to_db(file_path: str, db: AsyncSession = Depends(get_db)):
    df = pd.read_csv(file_path)
    table_name = os.path.splitext(os.path.basename(file_path))[0]

    async with db as session:
        async with session.begin():
            file_dal = FileStructureDAL(session)
            result_load_to_db = await file_dal._load_data_to_db(file_path, df)
    if result_load_to_db:
        return table_name
    return {"Ошибка": "Данные из csv файла не загружены в БД!"}


async def _get_tables(db: AsyncSession = Depends(get_db)):
    async with db as session:
        async with session.begin():
            file_dal = FileStructureDAL(session)
            tables = await file_dal._get_tables()
    return tables


ASCENDING_STATE = True


def _filtering_and_sorting_data(table: DataFrame,
                                filter_column: str,
                                filter_value: str,
                                sort_column: str,
                                ascending: bool = Query(None, alias="ascending"),
                                ) -> (DataFrame, list, bool):
    global ASCENDING_STATE

    # Определение списка столбцов содержащих числовые значения
    numeric_columns = table.select_dtypes(include=['int64', 'float64']).columns.tolist()

    columns_data = table

    if filter_column:
        # Определяем допустимые значения из выбранного столбца
        filter_column_values = table[filter_column].unique()
        filter_values = filter_column_values.tolist()

        if filter_value:
            # Филтрация таблицы по выбранному значению
            filter_value = filter_value
            if filter_column in numeric_columns:
                try:
                    # Преобразуем значение в числовой тип
                    filter_value = float(filter_value)
                    columns_data = table[table[filter_column] == filter_value]
                except ValueError:
                    pass
            else:
                columns_data = table[table[filter_column] == filter_value]
        else:
            # Если некорректное значение фильтра, показываем все данные
            columns_data = table
    else:
        filter_values = []

    if sort_column:
        if ascending is None:
            ASCENDING_STATE = ASCENDING_STATE
        else:
            ASCENDING_STATE = not ASCENDING_STATE

        # Применяем сортировку к отфильтрованным данным
        columns_data = columns_data.sort_values(by=sort_column,
                                                ascending=ASCENDING_STATE)
    else:
        columns_data = columns_data

    return (columns_data, filter_values, ASCENDING_STATE)
