import sqlite3
from .query import DATABASE_NAME, query_create_db, user_field, cities_field, TABLE_NAME


def create_db(db_name):
    with sqlite3.connect(db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(query_create_db)
            connection.commit()
        

# декоратор
def connect_db(func):
    def wrapper(*args, **kwargs):
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query_create_db)

            func(cursor=cursor, *args, **kwargs)
    return wrapper


class DataBase:

    def __new__(cls):
        bb = super().__new__(cls)
        create_db(DATABASE_NAME)
        return bb

    @connect_db
    def insert_city(self, cursor, user_id, city):
        cursor.execute(f'''
            INSERT INTO {TABLE_NAME} ({user_field}, {cities_field}) VALUES({user_id}, '{city}'
            );
        ''')
        

    @connect_db
    def get_cities(self, cursor, user_id):
        cursor.execute(f'''
            SELECT {cities_field} FROM {TABLE_NAME}
            WHERE {user_field}=={user_id};
        ''')
        data = cursor.fetchall()
        return data
        # for row in data:
        #     print(row)
    

