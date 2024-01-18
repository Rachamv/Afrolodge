from ..services.db_connection import connect_to_database

with connect_to_database() as (conn, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            country TEXT NOT NULL
        )
    """)

def create_state(name, country):
    """Adds a new state to the database."""
    with connect_to_database() as (conn, cursor):
        cursor.execute("""
            INSERT INTO states (name, country)
            VALUES (?, ?)
        """, (name, country))
        conn.commit()

def get_state_details(state_id):
    """Retrieves details about a specific state."""
    with connect_to_database() as (conn, cursor):
        cursor.execute("SELECT * FROM states WHERE id=?", (state_id,))
        state_data = cursor.fetchone()
    return state_data

def delete_state(state_id):
    """Removes a state and its associated data (if any)."""
    with connect_to_database() as (conn, cursor):
        cursor.execute("DELETE FROM states WHERE id=?", (state_id,))
        conn.commit()
