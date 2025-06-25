import mysql.connector
import numpy as np
from sqlalchemy import create_engine

# SQLAlchemy engine for pandas compatibility
engine = create_engine('mysql+mysqlconnector://root:@localhost/face_attendance')

def get_db_connection():
    """Create and return a new database connection"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="face_attendance"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def init_database():
    """Initialize database tables and default data"""
    conn = get_db_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    
    try:
        # Create tables if they don't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            roll_no VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(50) NOT NULL,
            face_encoding BLOB
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            roll_no VARCHAR(20) NOT NULL,
            subject_id INT NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            FOREIGN KEY (roll_no) REFERENCES students(roll_no),
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin', 'teacher') NOT NULL
        )""")

        # Insert default data
        default_subjects = ['Math', 'Science', 'Design']
        for subject in default_subjects:
            cursor.execute("INSERT IGNORE INTO subjects (name) VALUES (%s)", (subject,))

        default_users = [
            ('admin', 'admin123', 'admin'),
            ('teacher1', 'teacher123', 'teacher')
        ]
        for username, password, role in default_users:
            cursor.execute(
                "INSERT IGNORE INTO users (username, password, role) VALUES (%s, SHA2(%s, 256), %s)",
                (username, password, role)
            )

        conn.commit()
        return True

    except mysql.connector.Error as err:
        print(f"Database initialization error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def add_subject(subject_name):
    """Add a new subject to the database"""
    conn = get_db_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO subjects (name) VALUES (%s)",
            (subject_name,)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error adding subject: {err}")
        return False
    finally:
        cursor.close()

def get_subject_id(subject_name):
    """Get subject ID by name"""
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM subjects WHERE name = %s", (subject_name,))
        subject = cursor.fetchone()
        return subject[0] if subject else None
    except mysql.connector.Error as err:
        print(f"Error getting subject ID: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_subjects():
    """Get list of all subjects as dictionaries"""
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, name FROM subjects ORDER BY name")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error getting subjects: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def add_student(roll_no, name, face_encoding):
    """Add a new student to the database"""
    conn = get_db_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (roll_no, name, face_encoding) VALUES (%s, %s, %s)",
            (roll_no, name, face_encoding.tobytes())
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error adding student: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_students():
    """Get all students with their face encodings"""
    conn = get_db_connection()
    if not conn:
        return {}

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT roll_no, name, face_encoding FROM students")
        students = {}
        for row in cursor.fetchall():
            students[row['roll_no']] = {
                'name': row['name'],
                'encoding': np.frombuffer(row['face_encoding'], dtype=np.float64) if row['face_encoding'] else None
            }
        return students
    except mysql.connector.Error as err:
        print(f"Error getting students: {err}")
        return {}
    finally:
        cursor.close()
        conn.close()

def log_attendance(roll_no, subject_id):
    conn = get_db_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        from datetime import datetime
        now = datetime.now()
        
        # Store as proper DATE and TIME types
        cursor.execute(
            "INSERT INTO attendance (roll_no, subject_id, date, time) VALUES (%s, %s, %s, %s)",
            (str(roll_no), int(subject_id), now.date(), now.time())  # No .strftime() needed
        )
        conn.commit()
        return True
    except Exception as err:
        print(f"Error logging attendance: {err}")
        return False
    finally:
        cursor.close()
        conn.close()
def login(username, password):
    """Authenticate user"""
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT role FROM users WHERE username = %s AND password = SHA2(%s, 256)",
            (username, password)
        )
        user = cursor.fetchone()
        return user['role'] if user else None
    except mysql.connector.Error as err:
        print(f"Login error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

# Initialize database when this module is imported
init_database()