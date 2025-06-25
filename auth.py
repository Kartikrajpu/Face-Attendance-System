from getpass import getpass
from database import get_db_connection

def login():
    username = input("Username: ")
    password = getpass("Password: ")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role FROM users WHERE username = %s AND password = SHA2(%s, 256)",
        (username, password)
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None  # Returns 'admin' or 'teacher'