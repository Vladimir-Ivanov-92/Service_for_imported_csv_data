import pandas as pd
from fastapi import APIRouter, Request, UploadFile, File, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.service import _load_data, _get_tables, _get_name_columns_from_csv_table
from db.session import get_db

file_router = APIRouter()

# Templates
templates = Jinja2Templates(directory="templates")


# HTML страница с формой загрузки CSV файла
@file_router.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


# Загрузка CSV файла и формирование базы данных
@file_router.post('/upload')
async def upload_file(request: Request, file: UploadFile = File(...),
                      db: AsyncSession = Depends(get_db)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, 'wb') as f:
        f.write(file.file.read())
    table_name = await _load_data(file_path, db)
    # os.remove(file_path)
    return templates.TemplateResponse("upload_success.html",
                                      {"request": request, "table_name": table_name})


# HTML страница для отображения списка таблиц в базе данных
@file_router.get("/tables", response_class=HTMLResponse)
async def show_tables(request: Request, db: AsyncSession = Depends(get_db)):
    tables = await _get_tables(db)
    context = {"request": request, "tables": tables}
    return templates.TemplateResponse("all_tables.html", context)


ASCENDING_STATE = True


@file_router.get('/table/{table_name}', response_class=HTMLResponse)
async def sort_data(request: Request, table_name: str,
                    sort_column: str = Query(None, alias="sort_column"),
                    ascending: bool = Query(None, alias="ascending"),
                    filter_column: str = Query(None, alias="filter_column"),
                    filter_value: str = Query(None, alias="filter_value"),
                    db: AsyncSession = Depends(get_db)):
    global ASCENDING_STATE

    file_path = f"uploads/{table_name}.csv"
    table = pd.read_csv(file_path)
    name_columns = await _get_name_columns_from_csv_table(table, db)
    numeric_columns = table.select_dtypes(include=['int64', 'float64']).columns.tolist()
    columns_data = table

    if filter_column:
        # Применяем фильтрацию
        filter_column_values = table[filter_column].unique()
        filter_values = filter_column_values.tolist()

        if filter_value:
            filter_value = filter_value
            if filter_column in numeric_columns:
                try:
                    filter_value = float(
                        filter_value)  # Преобразуем значение в числовой тип
                    columns_data = table[table[filter_column] == filter_value]
                except ValueError:
                    pass
            else:
                columns_data = table[table[filter_column] == filter_value]
        else:
            columns_data = table  # Если некорректное значение фильтра, показываем все данные
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

    context = {"request": request, "table_name": table_name,
               "name_columns": name_columns, "columns_data": columns_data.iterrows(),
               "sort_column": sort_column,
               "filter_column": filter_column,
               "filter_value": filter_value,
               "filter_values": filter_values,
               "ascending": ASCENDING_STATE}
    return templates.TemplateResponse("data.html", context)
