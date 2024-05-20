from .repositories import *


class CityRepositoryService(CityRepository):
    def insert_city(self, user_id: int, city: str) -> None:
        user_cities = self.select(user_id=user_id)
        city_in_db = self.update(city=city, user_id=user_id, cities=user_cities)
        self.delete_first_by_date(cities=user_cities, user_id=user_id)
        if not city_in_db:
            self.insert(user_id=user_id, city=city)
     
    def get_cities(self, user_id: int) -> list:
        cities = self.select(user_id=user_id)
        return cities
