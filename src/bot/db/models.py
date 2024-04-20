import sqlite3
from aiosqlite3.cursor import Cursor
from .query import *
from datetime import datetime
import asyncio



async def create_db(db_name):
    async with sqlite3.connect(db_name) as connection:
        cursor = await connection.cursor()
        await cursor.execute(query_create_db)
        await connection.commit()
        

# декоратор
def connect_db(func):
    async def wrapper(*args, **kwargs):
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            print('cursor in dec: ', cursor)
            cursor.execute(query_create_db)
            res = await func(cursor=cursor, *args, **kwargs)
            print('res: ', res)
            return res
    return wrapper


class DataBase(AsyncQueryDb):
    
    @connect_db
    async def insert_city(self, cursor: Cursor, user_id: int, city: str) -> None:

        data = await asyncio.create_task(self.selectUserCities(cursor, user_id=user_id))
        c2 = await asyncio.create_task(self.t1(cursor, city, user_id, data))
        await asyncio.create_task(self.t2(cursor, data, user_id))
        if not c2:
            await asyncio.create_task(self.t3(cursor, user_id, city))
     
            

    @connect_db
    async def get_cities(self, cursor: Cursor, user_id: int) -> list:
        print('start get_cities in bd')
        cursor.execute(f'''
            SELECT {cities_field} FROM {TABLE_NAME}
            WHERE {user_field}=={user_id};
        ''')
        
        r_data = [replace_select_data(row) for row in cursor.fetchall()]
        print('r_data: ', r_data)
        return r_data

