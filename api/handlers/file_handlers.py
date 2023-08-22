import os

import pandas as pd
from fastapi import APIRouter, Request, UploadFile, File, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.service import _load_data, _get_tables, _get_name_columns_from_csv_table, \
    _get_columns_data_from_csv_table
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


# Получение данных из конкретной таблицы
@file_router.get('/table/{table_name}', response_class=HTMLResponse)
async def get_data(request: Request, table_name: str,
                   db: AsyncSession = Depends(get_db)):
    file_path = f"uploads/{table_name}.csv"
    table = pd.read_csv(file_path)
    name_columns = await _get_name_columns_from_csv_table(table, db)
    columns_data = await _get_columns_data_from_csv_table(table, db)
    context = {"request": request, "table_name": table_name,
               "name_columns": name_columns, "columns_data": columns_data}
    return templates.TemplateResponse("data.html", context)
