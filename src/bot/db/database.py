from dataclasses import dataclass


@dataclass
class DataBase:
    name: str
    table: "Table"

@dataclass
class Table:
    name: str
    user_field: int
    cities_field: str
    date_field: str