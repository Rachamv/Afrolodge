from ..services.db_connection import connect_to_database

with connect_to_database() as (conn, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS places (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            location TEXT NOT NULL,
            price REAL NOT NULL,
            amenities TEXT,
            photos TEXT,
            availability_calendar TEXT,
            host_id INTEGER NOT NULL,
            reviews JSON
        )
    """)

def create_place(title, description, location, price, amenities, photos, availability_calendar, host_id, reviews):
    """Adds a new place to the database."""
    with connect_to_database() as (conn, cursor):
        cursor.execute("""
            INSERT INTO places (title, description, location, price, amenities, photos, availability_calendar, host_id, reviews)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, description, location, price, amenities, photos, availability_calendar, host_id, reviews))
        conn.commit()

def get_place_details(place_id):
    """Retrieves detailed information about a place."""
    with connect_to_database() as (conn, cursor):
        cursor.execute("SELECT * FROM places WHERE id=?", (place_id,))
        place_data = cursor.fetchone()
    return place_data

def edit_place(place_id, **kwargs):
    """Modifies existing place information."""
    with connect_to_database() as (conn, cursor):
        update_query = "UPDATE places SET " + ", ".join([f"{key}=?" for key in kwargs]) + " WHERE id=?"
        cursor.execute(update_query, list(kwargs.values()) + [place_id])
        conn.commit()

def delete_place(place_id):
    """Removes a place listing."""
    with connect_to_database() as (conn, cursor):
        cursor.execute("DELETE FROM places WHERE id=?", (place_id,))
        conn.commit()

def user_add_place(user_id, title, description, location, price, amenities, photos, availability_calendar):
    """Allows a user to add their place for listing."""
    create_place(title, description, location, price, amenities, photos, availability_calendar, user_id, [])
