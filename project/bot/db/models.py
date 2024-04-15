import sqlite3
from .query import (DATABASE_NAME, TABLE_NAME, query_create_db,
                    user_field, cities_field, replace_select_data)


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

            return func(cursor=cursor, *args, **kwargs)
    return wrapper


class DataBase:

    def __new__(cls):
        create_db(DATABASE_NAME)
        return super().__new__(cls)

    @connect_db
    def insert_city(self, cursor, user_id, city):
        cursor.execute(f'''
            SELECT {cities_field} FROM {TABLE_NAME}
            WHERE {user_field} == {user_id}
        ''')
        cities = cursor.fetchall()
        for city_db in cities:
            if replace_select_data(city_db) == city:
                return
        
        cursor.execute(f'''
            INSERT INTO {TABLE_NAME} ({user_field}, {cities_field}) VALUES({user_id}, '{city}');
        ''')
        

    @connect_db
    def get_cities(self, cursor, user_id):
        cursor.execute(f'''
            SELECT {cities_field} FROM {TABLE_NAME}
            WHERE {user_field}=={user_id};
        ''')
        data = cursor.fetchall()
        
        r_data = [replace_select_data(row) for row in data]
        print('model', r_data)
        print(r_data)
        return r_data

