from .config import (
    database_name,
    table_name,
    user_field,
    cities_field,
    date_field,
)
from sqlite3 import connect
from .database import DataBase, Table


def init_db() -> None:
    query_create_db = (f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {user_field} TEXT NOT NULL,
                    {cities_field} TEXT NOT NULL,
                    {date_field} TIMESTAMP)
            ''')
    
    with connect(database_name) as connection:
        cursor = connection.cursor()
        cursor.execute(query_create_db)
        connection.commit()


def create_db_model() -> DataBase:
    return DataBase(
        database_name,
        Table(
            table_name,
            user_field,
            cities_field,
            date_field,
        ),
    )