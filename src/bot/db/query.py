from typing import AnyStr

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
    async def selectUserCities(self, cursor, user_id):
        await cursor.execute(f'''
            SELECT {cities_field} FROM {TABLE_NAME}
            WHERE {user_field} == {user_id}
            ORDER BY {date_field} 
        ''')
    
    