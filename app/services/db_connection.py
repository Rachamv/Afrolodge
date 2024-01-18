import sqlite3

def connect_to_database():
    """Creates a database connection and returns a cursor.

    Returns:
        tuple: (connection, cursor)
    """

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        return conn, cursor

def execute_query(query, params=None):
    """Executes a query with optional parameters.

    Args:
        query (str): The SQL query to execute.
        params (tuple, optional): Parameters to substitute into the query. Defaults to None.

    Returns:
        list: The results of the query, if any.
    """

    conn, cursor = connect_to_database()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        conn.commit()  # Commit changes only if execution was successful
        return results
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()  # Ensure cursor is closed even in case of errors
