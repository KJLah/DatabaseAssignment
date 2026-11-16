"""
students_app.py file

A small command-line application that connects to a PostgreSQL database
and performs CRUD (Create, Read, Update, Delete) operations on the
"students" table.

Connection settings are read from environment variables so no password
is hard-coded in the source (check README.md).
"""

import os
import sys

import psycopg2
from psycopg2 import errors


# ------------------------------------------------------------
# Database connection
# ------------------------------------------------------------

# Connection parameters. Each one can be overridden with an environment
# variable; otherwise the default (a local PostgreSQL install) is used.
DB_CONFIG = {
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", "5432"),
    "dbname": os.getenv("PGDATABASE", "students_db"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.getenv("PGPASSWORD", ""),
}


def get_connection():
    """Open and return a new connection to the PostgreSQL database."""
    return psycopg2.connect(**DB_CONFIG)


# ------------------------------------------------------------
# CRUD functions
# ------------------------------------------------------------

def getAllStudents():
    """READ: retrieve every row in the students table and print it."""
    sql = """
        SELECT student_id, first_name, last_name, email, enrollment_date
        FROM students
        ORDER BY student_id;
    """
    # "with" closes the cursor automatically; the connection is closed
    # in the finally block.
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
    finally:
        conn.close()

    # Print the results as a simple table.
    print(f"\n{'ID':<4} {'First':<12} {'Last':<12} {'Email':<28} {'Enrolled'}")
    print("-" * 70)
    for student_id, first, last, email, enrolled in rows:
        print(f"{student_id:<4} {first:<12} {last:<12} {email:<28} {enrolled or ''}")
    print(f"({len(rows)} student(s))\n")
    return rows

def addStudent(first_name, last_name, email, enrollment_date):
    """CREATE: insert a new student and return the generated student_id."""
    # Parameters (%s) are passed separately so psycopg2 escapes them,
    # which prevents SQL injection.
    sql = """
        INSERT INTO students (first_name, last_name, email, enrollment_date)
        VALUES (%s, %s, %s, %s)
        RETURNING student_id;
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (first_name, last_name, email, enrollment_date or None))
            new_id = cur.fetchone()[0]
        conn.commit()  # make the insert permanent
        print(f"Added student {first_name} {last_name} with id {new_id}.")
        return new_id
    except errors.UniqueViolation:
        conn.rollback()
        print(f"Error: the email '{email}' is already used by another student.")
    except (errors.InvalidDatetimeFormat, errors.DatetimeFieldOverflow):
        conn.rollback()
        print(f"Error: '{enrollment_date}' is not a valid date (use YYYY-MM-DD).")
    except errors.NotNullViolation:
        conn.rollback()
        print("Error: first name, last name and email are all required.")
    finally:
        conn.close()
    return None

def updateStudentEmail(student_id, new_email):
    """UPDATE: change the email of the student with the given student_id."""
    sql = "UPDATE students SET email = %s WHERE student_id = %s;"
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (new_email, student_id))
            updated = cur.rowcount  # number of rows changed
        conn.commit()
        if updated:
            print(f"Updated email of student {student_id} to {new_email}.")
        else:
            print(f"No student found with id {student_id}.")
        return updated > 0
    except errors.UniqueViolation:
        conn.rollback()
        print(f"Error: the email '{new_email}' is already used by another student.")
    finally:
        conn.close()
    return False


def deleteStudent(student_id):
    """DELETE: remove the student with the given student_id."""
    sql = "DELETE FROM students WHERE student_id = %s;"
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (student_id,))
            deleted = cur.rowcount
        conn.commit()
    finally:
        conn.close()

    if deleted:
        print(f"Deleted student {student_id}.")
    else:
        print(f"No student found with id {student_id}.")
    return deleted > 0