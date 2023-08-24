# FastAPI service for working with imported data of csv format

### В данном проекте использовались следущие инструменты:

  - Python v3.11
  - fastapi v0.100
  - pandas v2.0
  - pydantic v2.1
  - sqlalchemy v1.4
  - alembic v1.11
  - pytest v7.4
  - poetry

## Setup and run:
Перейдите в директорию, в которую будете клонировать репозиторий.
В зависимости от того, каким менеджером зависимостей Вы пользуетесь, выполните следующие
команды:

При управлении зависимостями через [poetry](https://python-poetry.org/):
```bash
git clone https://github.com/Vladimir-Ivanov-92/Service_for_imported_csv_data.git
cd Service_for_imported_csv_data 
poetry install --without dev
poetry shell
make up
alembic upgrade heads
mkdir uploads
uvicorn run:app --reload
```

С помощью pip:
```bash
git clone https://github.com/Vladimir-Ivanov-92/Service_for_imported_csv_data.git
cd Service_for_imported_csv_data
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
make up
alembic upgrade heads
mkdir uploads
uvicorn run:app --reload
```

