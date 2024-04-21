import sqlite3
from .query import *
import asyncio



async def create_db(db_name) -> None:
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute(query_create_db)
        connection.commit()
        

# декоратор
def connect_db(func):
    async def wrapper(*args, **kwargs):
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(query_create_db)
            res = await func(cursor=cursor, *args, **kwargs)
            return res
    return wrapper


class DataBase(AsyncQueryDb):
    
    @connect_db
    async def insert_city(self, cursor, user_id: int, city: str) -> None:
        user_cities = await asyncio.create_task(self.selectUserCities(cursor, user_id=user_id))
        city_in_db = await asyncio.create_task(self.update_city(cursor, city, user_id, user_cities))
        await asyncio.create_task(self.delete_first_city(cursor, user_cities, user_id))
        if not city_in_db:
            await asyncio.create_task(self.insert(cursor, user_id, city))
     
            

    @connect_db
    async def get_cities(self, cursor, user_id: int) -> list:
        cities = await asyncio.create_task(self.selectUserCities(cursor, user_id))
        return cities

