import pandas as pd
from fastapi import APIRouter, Request, UploadFile, File, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.file.file_service import _load_data_from_csv_to_db, _get_tables, \
    _load_csv_to_uploads, _filtering_and_sorting_data
from db.session import get_db

file_router = APIRouter()

# Templates
templates = Jinja2Templates(directory="templates")


# HTML страница с формой загрузки CSV файла
@file_router.get("/", response_class=HTMLResponse)
def show_form(request: Request):
    """Отображение страницы загрузки файла"""
    return templates.TemplateResponse("upload.html", {"request": request})


# Загрузка CSV файла и формирование базы данных
@file_router.post('/upload')
async def upload_file(request: Request, file: UploadFile = File(...),
                      db: AsyncSession = Depends(get_db)):
    """
    Сохранение csv файла в папку uploads,
    запись данных о таблице в БД (таблица 'files')
    и отображение результата загрузки.
    """
    file_path = _load_csv_to_uploads(file)
    table_name = await _load_data_from_csv_to_db(file_path, db)
    # os.remove(file_path)
    return templates.TemplateResponse("upload_success.html",
                                      {"request": request, "table_name": table_name})


# HTML страница для отображения списка таблиц в базе данных
@file_router.get("/tables", response_class=HTMLResponse)
async def show_tables(request: Request, db: AsyncSession = Depends(get_db)):
    tables = await _get_tables(db)
    context = {"request": request, "tables": tables}
    return templates.TemplateResponse("all_tables.html", context)


@file_router.get('/table/{table_name}', response_class=HTMLResponse)
def sort_data(request: Request, table_name: str,
                    sort_column: str = Query(None, alias="sort_column"),
                    ascending: bool = Query(None, alias="ascending"),
                    filter_column: str = Query(None, alias="filter_column"),
                    filter_value: str = Query(None, alias="filter_value")):
    file_path = f"uploads/{table_name}.csv"
    table = pd.read_csv(file_path)

    # Получение имен столбцов таблицы
    name_columns = table.columns

    columns_data, filter_values, ascending = _filtering_and_sorting_data(table,
                                                                         filter_column,
                                                                         filter_value,
                                                                         sort_column,
                                                                         ascending)

    context = {"request": request, "table_name": table_name,
               "name_columns": name_columns,
               "columns_data": columns_data.iterrows(),
               "sort_column": sort_column,
               "filter_column": filter_column,
               "filter_value": filter_value,
               "filter_values": filter_values,
               "ascending": ascending}
    return templates.TemplateResponse("data.html", context)
