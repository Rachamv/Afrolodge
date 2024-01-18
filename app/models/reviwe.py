from ..services.db_connection import connect_to_database

with connect_to_database() as (conn, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Review (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            rating INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            place_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES User(id),
            FOREIGN KEY (place_id) REFERENCES Place(id)
        )
    """)

def create_review(content, rating, author_id, place_id):
    """Adds a new review to the database."""
    with connect_to_database() as (conn, cursor):
        cursor.execute("""
            INSERT INTO Review (content, rating, author_id, place_id)
            VALUES (?, ?, ?, ?)
        """, (content, rating, author_id, place_id))
        conn.commit()

def get_place_reviews(place_id):
    """Retrieves reviews for a specific place."""
    with connect_to_database() as (conn, cursor):
        cursor.execute("SELECT * FROM Review WHERE place_id=?", (place_id,))
        reviews = cursor.fetchall()
    return reviews

def delete_review(review_id):
    """Removes a user's review."""
    with connect_to_database() as (conn, cursor):
        cursor.execute("DELETE FROM Review WHERE id=?", (review_id,))
        conn.commit()
