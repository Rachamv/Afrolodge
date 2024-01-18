from ..services.db_connection import connect_to_database

class City:
    def __init__(self, name, state, country):
        self.name = name
        self.state = state
        self.country = country

    def create_city(self):
        with connect_to_database() as (conn, cursor):
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    state TEXT NOT NULL,
                    country TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                INSERT INTO cities (name, state, country)
                VALUES (?, ?, ?)
            ''', (self.name, self.state, self.country))
            conn.commit()

    def get_city_details(self, city_id):
        with connect_to_database() as (cursor):
            cursor.execute('''
                SELECT * FROM cities
                WHERE id = ?
            ''', (city_id,))
            city_data = cursor.fetchone()
        return city_data

    def delete_city(self, city_id):
        with connect_to_database() as (conn, cursor):
            cursor.execute('''
                DELETE FROM cities
                WHERE id = ?
            ''', (city_id,))
            conn.commit()