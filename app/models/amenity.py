from ..services.db_connection import connect_to_database

with connect_to_database() as (conn, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Amenity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    """)

def create_amenity(name, description):
    """Adds a new amenity to the database."""
    with connect_to_database() as (conn, cursor):
        cursor.execute("""
            INSERT INTO Amenity (name, description)
            VALUES (?, ?)
        """, (name, description))
        conn.commit()

def get_amenity_details(amenity_id):
    """Retrieves details about a specific amenity."""
    with connect_to_database() as (conn, cursor):
        cursor.execute("SELECT * FROM Amenity WHERE id=?", (amenity_id,))
        amenity_data = cursor.fetchone()
    return amenity_data

def delete_amenity(amenity_id):
    """Removes an amenity from the system."""
    with connect_to_database() as (conn, cursor):
        cursor.execute("DELETE FROM Amenity WHERE id=?", (amenity_id,))
        conn.commit()
