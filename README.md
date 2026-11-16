# Students Database – PostgreSQL CRUD Application

A Python command-line application that connects to a PostgreSQL database and
performs CRUD (Create, Read, Update, Delete) operations on a `students` table.

**Demo video:** <PASTE YOUR VIDEO LINK HERE>

## Repository structure

```text
.
├── application/
│   ├── students_application.py
│   └── requirements.txt
├── database/
│   └── schema.sql
├── .gitignore
└── README.md
```
## Requirements

- Python 3.8 or newer
- PostgreSQL
- pgAdmin
- A running PostgreSQL server

## Setup

## 1. Download the Project

```sh
git clone https://github.com/KJLah/DatabaseAssignment.git
cd DatabaseAssignment
```

## 2. Set Up the Database

1. Open pgAdmin and connect to your PostgreSQL server.
2. Right-click **Databases → Create → Database**.
3. Name the database `students_db` and save it.
4. Open the **Query Tool** for `students_db`.
5. Open `database/schema.sql` and execute the complete script.
6. Confirm the initial data using:

```sql
SELECT * FROM students ORDER BY student_id;
```

The table should contain:

| First name | Last name | Email | Enrollment date |
| --- | --- | --- | --- |
| John | Doe | john.doe@example.com | 2023-09-01 |
| Jane | Smith | jane.smith@example.com | 2023-09-01 |
| Jim | Beam | jim.beam@example.com | 2023-09-02 |

The schema provides an auto-incrementing integer primary key, required
names, a required unique email, and an optional enrollment date.

Run the setup script once in a fresh database. It does not replace an
existing students table. If rerunning it causes an aborted transaction,
execute `ROLLBACK;` before running other queries.

### 3. Install the Python dependency

```bash
python -m pip install -r application/requirements.txt
```

### 4. Set your connection settings

The app reads these environment variables (defaults in brackets):

| Variable     | Default       |
|--------------|---------------|
| `PGHOST`     | `localhost`   |
| `PGPORT`     | `5432`        |
| `PGDATABASE` | `students_db` |
| `PGUSER`     | `postgres`    |
| `PGPASSWORD` | *(empty)*     |

Usually you only need to set your password:

Windows PowerShell:

```powershell
$env:PGPASSWORD = "your_postgres_password"
```

Windows Command Prompt:

```cmd
set "PGPASSWORD=your_postgres_password"
```

macOS/Linux:

```sh
export PGPASSWORD='your_postgres_password'
```

Replace the example password with your PostgreSQL password. Run the
application from the same terminal where you set this variable.

## Running the application

```bash
python application/students_application.py
```

A menu appears:

```
1. Show all students
2. Add a student
3. Update a student's email
4. Delete a student
0. Exit
```

## Functions

| Function | What it does |
|----------|--------------|
| `getAllStudents()` | Runs `SELECT` on `students` and prints every row, ordered by id. |
| `addStudent(first_name, last_name, email, enrollment_date)` | Runs `INSERT` and prints the new `student_id`. Reports a duplicate email or invalid date instead of crashing. |
| `updateStudentEmail(student_id, new_email)` | Runs `UPDATE` on the given student. Reports if the id doesn't exist or the email is already taken. |
| `deleteStudent(student_id)` | Runs `DELETE` on the given student. Reports if the id doesn't exist. |

All queries use parameterized statements (`%s`) to prevent SQL injection, and
each change is committed so it is visible in pgAdmin right away.
