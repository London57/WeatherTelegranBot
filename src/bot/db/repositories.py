from typing import AnyStr
from datetime import datetime
import sqlite3
from .config import database_name
from .database import DataBase


def connect_db(func):
    def wrapper(*args, **kwargs):
        with sqlite3.connect(database_name) as connection:
            cursor = connection.cursor()
            res = func(cursor=cursor, *args, **kwargs)
            return res
    return wrapper

def replace_select_data(data: tuple):
    return str(data).replace("('",'').replace("',)", '')

            
class CityRepository:
    def __init__(self, db: DataBase):
        self.db = db
    
    @connect_db
    def select(self, cursor, user_id: int) -> list:
        cursor.execute(f'''
            SELECT {self.db.table.cities_field} FROM {self.db.table.name}
            WHERE {self.db.table.user_field} == {user_id}
            ORDER BY {self.db.table.date_field} 
        ''')
        data = cursor.fetchall()
        cities = [replace_select_data(row) for row in data]
        return cities

    @connect_db
    def insert(self, cursor, user_id: int, city: str) -> None:
        cursor.execute(f'''
        INSERT INTO {self.db.table.name} 
        ({self.db.table.user_field}, {self.db.table.cities_field}, {self.db.table.date_field})
        VALUES({user_id}, '{city}', '{datetime.now()}');
    ''')    
        
    @connect_db
    def update(self, cursor, city: str, user_id: int, cities: list)-> bool:
        if cities:
            for city_db in cities:
                city_db = replace_select_data(city_db)
                if city_db == city:
                    cursor.execute(F'''
                        UPDATE {self.db.table.name} 
                        SET {self.db.table.date_field} == '{datetime.now()}'
                        WHERE {self.db.table.user_field} == {user_id} and {self.db.table.cities_field} == '{city_db}'
                    ''')
                    return 1
    
    @connect_db
    def delete_first_by_date(self, cursor, cities: list, user_id: int) -> None:
        if len(cities) > 3:
            cursor.execute(f'''
                DELETE FROM {self.db.table.name}
                WHERE {self.db.table.user_field} == {user_id} and {self.db.table.cities_field} == '{cities[0]}';
            ''')
    
