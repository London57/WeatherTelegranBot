from typing import AnyStr

DATABASE_NAME = 'sqlite3.db'
TABLE_NAME = 'User_cities'


user_field: AnyStr = 'user_id'
cities_field: AnyStr = 'city'

query_create_db = (f'''
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {user_field} TEXT NOT NULL,
                    {cities_field} TEXT NOT NULL UNIQUE)
            ''')