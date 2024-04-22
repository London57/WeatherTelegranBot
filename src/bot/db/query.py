from typing import AnyStr
from datetime import datetime

DATABASE_NAME = 'sqlite3.db'
TABLE_NAME = 'User_cities'


user_field: AnyStr = 'user_id'
cities_field: AnyStr = 'city'
date_field = 'date_update'

query_create_db = (f'''
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {user_field} TEXT NOT NULL,
                    {cities_field} TEXT NOT NULL,
                    {date_field} TIMESTAMP)
            ''')

def replace_select_data(data: tuple):
    return str(data).replace("('",'').replace("',)", '')


class AsyncQueryDb:

    async def selectUserCities(self, cursor, user_id: int) -> list:
        cursor.execute(f'''
            SELECT {cities_field} FROM {TABLE_NAME}
            WHERE {user_field} == {user_id}
            ORDER BY {date_field} 
        ''')
        data = cursor.fetchall()
        cities = [replace_select_data(row) for row in data]
        return cities
    
    async def update_city(self, cursor, city: str, user_id: int, cities: list)-> bool:
            if cities:
                for city_db in cities:
                    city_db = replace_select_data(city_db)
                    if city_db == city:
                        cursor.execute(F'''
                            UPDATE {TABLE_NAME} 
                            SET {date_field} == '{datetime.now()}'
                            WHERE {user_field} == {user_id} and {cities_field} == '{city_db}'
                        ''')
                        return 1
                    
    async def delete_first_city(self, cursor, cities: list, user_id: int) -> None:
        if len(cities) > 3:
            cursor.execute(f'''
                DELETE FROM {TABLE_NAME}
                WHERE {user_field} == {user_id} and {cities_field} == '{cities[0]}';
            ''')
                
    async def insert(self, cursor, user_id: int, city: str) -> None:
            cursor.execute(f'''
            INSERT INTO {TABLE_NAME} 
            ({user_field}, {cities_field}, {date_field})
            VALUES({user_id}, '{city}', '{datetime.now()}');
        ''')