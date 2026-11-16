"""A simple PostgreSQL application for managing students."""

import os
from contextlib import closing
from datetime import date

import psycopg2


def run_query(sql, values=()):
    """Run SQL safely, commit or roll back, and close the connection."""
    with closing(psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "students_db"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", ""),
        connect_timeout=5,
    )) as conn:
        # This context commits on success and rolls back on error.
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, values)
                return cursor.fetchall()


def required(value):
    """Remove surrounding spaces and reject empty names or emails."""
    if value is None or not value.strip():
        raise ValueError("Names and email cannot be blank.")
    return value.strip()


def getAllStudents():
    """Retrieve and display every student."""
    rows = run_query(
        "SELECT student_id, first_name, last_name, email, enrollment_date "
        "FROM students ORDER BY student_id"
    )

    print("ID | First name | Last name | Email | Enrollment date")
    for row in rows:
        print(" | ".join("" if value is None else str(value) for value in row))
    print(f"({len(rows)} students)")
    return rows


def addStudent(first_name, last_name, email, enrollment_date):
    """Insert a student and return the generated ID."""
    first_name = required(first_name)
    last_name = required(last_name)
    email = required(email)

    # A blank enrollment date becomes SQL NULL.
    if isinstance(enrollment_date, str):
        enrollment_date = enrollment_date.strip()
        enrollment_date = (
            date.fromisoformat(enrollment_date) if enrollment_date else None
        )

    rows = run_query(
        "INSERT INTO students (first_name, last_name, email, enrollment_date) "
        "VALUES (%s, %s, %s, %s) RETURNING student_id",
        (first_name, last_name, email, enrollment_date),
    )

    student_id = rows[0][0]
    print(f"Added student with ID {student_id}.")
    return student_id


def updateStudentEmail(student_id, new_email):
    """Update a student's email and report whether the ID exists."""
    rows = run_query(
        "UPDATE students SET email = %s "
        "WHERE student_id = %s RETURNING student_id",
        (required(new_email), student_id),
    )

    print("Email updated." if rows else "Student not found.")
    return bool(rows)


def deleteStudent(student_id):
    """Delete a student and report whether the ID exists."""
    rows = run_query(
        "DELETE FROM students WHERE student_id = %s RETURNING student_id",
        (student_id,),
    )

    print("Student deleted." if rows else "Student not found.")
    return bool(rows)


def read_id():
    """Read a positive student ID; invalid input is handled by the menu."""
    student_id = int(input("Student ID: "))
    if student_id < 1:
        raise ValueError("Student ID must be positive.")
    return student_id


def main():
    """Display the menu and handle input or database errors."""
    while True:
        print(
            "\n1. Show students"
            "\n2. Add student"
            "\n3. Update email"
            "\n4. Delete student"
            "\n0. Exit"
        )

        try:
            choice = input("Choose an option: ").strip()

            if choice == "0":
                return
            elif choice == "1":
                getAllStudents()
            elif choice == "2":
                addStudent(
                    input("First name: "),
                    input("Last name: "),
                    input("Email: "),
                    input("Enrollment date (YYYY-MM-DD, blank for none): "),
                )
            elif choice == "3":
                updateStudentEmail(read_id(), input("New email: "))
            elif choice == "4":
                deleteStudent(read_id())
            else:
                print("Choose an option from 0 to 4.")

        except ValueError as error:
            print(f"Invalid input: {error}")
        except psycopg2.errors.UniqueViolation:
            print("That email is already used by another student.")
        except psycopg2.OperationalError:
            print("Cannot connect. Check PostgreSQL and your PG settings.")
        except psycopg2.Error:
            print("Database error. Check that database/schema.sql has been run.")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return


if __name__ == "__main__":
    main()