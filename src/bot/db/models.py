import aiosqlite3
from aiosqlite3.cursor import Cursor
from .query import *
from datetime import datetime
import time



async def create_db(db_name):
    async with aiosqlite3.connect(db_name) as connection:
        cursor = await connection.cursor()
        await cursor.execute(query_create_db)
        await connection.commit()
        

# декоратор
def connect_db(func):
    async def wrapper(*args, **kwargs):
        async with aiosqlite3.connect(DATABASE_NAME) as connection:
            cursor = await connection.cursor()
            print('cursor in dec: ', cursor)
            await cursor.execute(query_create_db)
            res = await func(cursor=cursor, *args, **kwargs)
            print('res: ', res)
            return res
    return wrapper


class DataBase(AsyncQueryDb):

    @connect_db
    async def insert_city(self, cursor: Cursor, user_id: int, city: str) -> None:
        
        
        data = await cursor.fetchall()
        print('data: ', data)
        cities = [replace_select_data(row) for row in data]
        print('data после', cities)
        if cities:
            for city_db in cities:
                city_db = replace_select_data(city_db)
                if city_db == city:
                    print('city_db::::::::')
                    await cursor.execute(F'''
                        UPDATE {TABLE_NAME} 
                        SET {date_field} == '{datetime.now()}'
                        WHERE {user_field} == {user_id} and {cities_field} == '{city_db}'
                    ''')
                    return
            if len(cities) > 3:
                await cursor.execute(f'''
                    DELETE FROM {TABLE_NAME}
                    WHERE {user_field} == {user_id} and {cities_field} == '{cities[0]}';
                ''')
                return
        print('::::::::::::::')
    
        await cursor.execute(f'''
            INSERT INTO {TABLE_NAME} 
            ({user_field}, {cities_field}, {date_field})
            VALUES({user_id}, '{city}', '{datetime.now()}');
        ''')
        
        print(':::::::')
     
            

    @connect_db
    async def get_cities(self, cursor: Cursor, user_id: int) -> list:
        print('start get_cities in bd')
        await cursor.execute(f'''
            SELECT {cities_field} FROM {TABLE_NAME}
            WHERE {user_field}=={user_id};
        ''')
        
        r_data = [replace_select_data(row) for row in await cursor.fetchall()]
        print('r_data: ', r_data)
        return r_data

