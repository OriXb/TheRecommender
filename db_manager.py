import sqlite3
import os

# Create path for database.
db_directory = os.path.join(os.getcwd(), "data_base")
db_file = "data_base.db"  # שם הקובץ למסד הנתונים
db_path = os.path.join(db_directory, db_file)  # יצירת הנתיב המלא

# If first time and database don't exists-create it.
if not os.path.exists(db_directory):
    os.makedirs(db_directory)


def execute_sql(sql: str):
    """
    Simple sql sender.
    """
    cursor.execute(sql)


def create_tables():
    """
    Create required tables for the program to work if not exists.
    """

    execute_sql("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        is_active INTEGER DEFAULT 0
    )
    """)

    execute_sql("""
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre_name TEXT UNIQUE NOT NULL
    )
    """)

    execute_sql("""
    CREATE TABLE IF NOT EXISTS directors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        director_name TEXT UNIQUE NOT NULL
    )
    """)

    execute_sql("""
    CREATE TABLE IF NOT EXISTS actors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        actor_name TEXT UNIQUE NOT NULL
    )
    """)

    execute_sql("""
    CREATE TABLE IF NOT EXISTS languages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        language_name TEXT UNIQUE NOT NULL
    )
    """)

    execute_sql("""
    CREATE TABLE IF NOT EXISTS content_origins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origin_name TEXT UNIQUE NOT NULL
    )
    """)

    # GENRES
    execute_sql("""
    CREATE TABLE IF NOT EXISTS genresForUsers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        genre_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (genre_id) REFERENCES genres (id)
    )
    """)

    # DIRECTORS
    execute_sql("""
    CREATE TABLE IF NOT EXISTS directorsForUsers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        director_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (director_id) REFERENCES directors (id)
    )
        """)

    # ACTORS
    execute_sql("""
        CREATE TABLE IF NOT EXISTS actorsForUsers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            actor_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (actor_id) REFERENCES actors (id)
        )
            """)

    # LANGS
    execute_sql("""
        CREATE TABLE IF NOT EXISTS languagesForUsers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            language_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (language_id) REFERENCES languages (id)
        )
            """)

    # ORIGIN
    execute_sql("""
        CREATE TABLE IF NOT EXISTS originsForUsers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            origin_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (origin_id) REFERENCES content_origins (id)
        )
            """)

    connection.commit()


# Create connection to database, and create database if not exists (first time or deleted).
connection = sqlite3.connect(db_path)
cursor = connection.cursor()
create_tables()


def add_new_user(username: str, password: str):
    """
    Add new user to the database.
    """
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

    connection.commit()


def is_username_taken(username: str) -> bool:
    """
    Check if username already taken.
    """
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    return user is not None


def is_user_valid(username: str, password: str):
    """
    Check if username and password match and exists in the database.
    """
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False


def get_user_id(username: str):
    """
    Return user id by username.
    """
    cursor.execute("SELECT id FROM users WHERE username = ?", username)
    return cursor.fetchone()


def is_user_active(user_id: str):
    """
    Return if user is active (means that he finished the setup).
    """
    cursor.execute("SELECT is_active FROM users WHERE id = ?", user_id)
    data = cursor.fetchone()
    if data == 0:
        return False
    elif data == 1:
        return True


def print_users_test():
    """
    Temp commend- TEST
    """
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
