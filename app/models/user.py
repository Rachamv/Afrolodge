from ..services.db_connection import connect_to_database

class User:
    def __init__(self, email, password, name, profile_picture=None):
        self.email = email
        self.password = password
        self.name = name
        self.profile_picture = profile_picture

    def create_user(self):
        with connect_to_database() as (conn, cursor):
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    name TEXT NOT NULL,
                    profile_picture TEXT
                )
            """)
            cursor.execute("INSERT INTO users (email, password, name, profile_picture) VALUES (?, ?, ?, ?)",
                           (self.email, self.password, self.name, self.profile_picture))
            conn.commit()

    @classmethod
    def authenticate_user(cls, email, password):
        with connect_to_database() as (cursor):
            cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            user_data = cursor.fetchone()
            if user_data:
                return cls(*user_data)  # Create a User instance from fetched data
            return None

    def update_user(self):
        with connect_to_database() as (conn, cursor):
            cursor.execute("UPDATE users SET name=?, profile_picture=? WHERE email=?",
                           (self.name, self.profile_picture, self.email))
            conn.commit()

    def delete_user(self):
        with connect_to_database() as (conn, cursor):
            cursor.execute("DELETE FROM users WHERE email=?", (self.email,))
            conn.commit()
