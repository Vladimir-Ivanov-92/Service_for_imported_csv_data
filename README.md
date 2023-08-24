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

Docs: 
![docs.png](image_readme%2Fdocs.png)

Пример работы:
1. Загрузка csv файла: (/file)
![Загрузка CSV.png](image_readme%2F%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B0%20CSV.png)
2. Список всех загруженных таблиц: (/file/tables)
![Таблицы.png](image_readme%2F%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D1%8B.png)
3. Данные из выбранной таблицы: (/file/table/titanic)
![Таблица (общие данные).png](image_readme%2F%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20%28%D0%BE%D0%B1%D1%89%D0%B8%D0%B5%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5%29.png)
4. Отсортированные данные по столбцу Pclass: (file/table/titanic?sort_column=Pclass&ascending=True)
![Таблица + сортировка.png](image_readme%2F%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20%2B%20%D1%81%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0.png)
5. Выбор фильтра таблицы по столбцу и значению: 
![Фильтр 2.png](image_readme%2F%D0%A4%D0%B8%D0%BB%D1%8C%D1%82%D1%80%202.png)
6. Данные из таблицы в соответсвии с выбранным фильтром (/file/table/titanic?filter_column=Pclass&filter_value=3)
![Таблица + фильтр.png](image_readme%2F%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20%2B%20%D1%84%D0%B8%D0%BB%D1%8C%D1%82%D1%80.png)
7. Данные из таблицы в соответсвии с выбранным фильтром + сортировка по столбцу Age: (/file/table/titanic?sort_column=Age&ascending=False&filter_column=Pclass&filter_value=3)
![Таблица + фильтр + сортировка.png](image_readme%2F%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20%2B%20%D1%84%D0%B8%D0%BB%D1%8C%D1%82%D1%80%20%2B%20%D1%81%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0.png)