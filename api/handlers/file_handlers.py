import os

from fastapi import APIRouter, Request, UploadFile, File, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.service import _load_data, _get_tables
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
    return templates.TemplateResponse("tables.html", context)