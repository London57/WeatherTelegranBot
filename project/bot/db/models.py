import sqlite3
from .fields import DATABASE_NAME, TABLE_NAME, username_field, cities_field

persistent_data = (TABLE_NAME, username_field, cities_field)

#функция для connect
def create_db(db_name):
    with sqlite3.connect(db_name) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ?(
                        id INTEGER PRYMARY KEY AUTOINCREMENT,
                        ? TEXT NOT NULL
                        ? TEXT NOT NULL,
                )
            ''', persistent_data)
    

# декоратор
def connect_db(func):
    def wrapper(*args, **kwargs):
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ?(
                        id INTEGER PRYMARY KEY,
                        ? TEXT NOT NULL
                        ? TEXT NOT NULL,
                )
            ''', persistent_data)
            func(cursor, *args, **kwargs)
    return wrapper


class Bd:
    def __call__(self):
        create_db(DATABASE_NAME)


    # @connect_db
    # def insert_cities(cursor, user, cities):
    #     cursor.execut('''
    #         INSERT INTO ? VALUES(?, ?)
    #     ''')


    @connect_db
    def get_cities(cursor, user):
        data = cursor.execute('''
            SELECT cities FROM ?
            WHERE username==?
        ''', user)
        return data