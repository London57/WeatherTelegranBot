import sqlite3
from .query import *
from datetime import datetime


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
            ORDER BY {date_field} 
        ''')
        
        cities = [replace_select_data(row) for row in cursor.fetchall()]

        for city_db in cities:
            city_db = replace_select_data(city_db)
            if city_db == city:
                cursor.execute(F'''
                    UPDATE {TABLE_NAME} 
                    SET {date_field} == '{datetime.now()}'
                    WHERE {user_field} == {user_id} and {cities_field} == '{city_db}'
                ''')
        print(cities, type(cities))
        if len(cities) > 3:
            cursor.execute(f'''
                DELETE FROM {TABLE_NAME}
                WHERE {user_field} == {user_id} and {cities_field} == '{cities[0]}';
            ''')
        cursor.execute(f'''
            INSERT INTO {TABLE_NAME} 
            ({user_field}, {cities_field}, {date_field})
            VALUES({user_id}, '{city}', '{datetime.now()}');
        ''')
        

    @connect_db
    def get_cities(self, cursor, user_id):
        cursor.execute(f'''
            SELECT {cities_field} FROM {TABLE_NAME}
            WHERE {user_field}=={user_id};
        ''')
        
        r_data = [replace_select_data(row) for row in cursor.fetchall()]
        print(r_data)
        return r_data

