# Students Database – PostgreSQL CRUD Application

A Python command-line application that connects to a PostgreSQL database and
performs CRUD (Create, Read, Update, Delete) operations on a `students` table.

**Demo video:** <PASTE YOUR VIDEO LINK HERE>

## Repository structure

```
.
├── db/
│   └── schema.sql          # creates the students table and inserts the initial data
├── app/
│   ├── students_app.py     # the application (all four CRUD functions + menu)
│   └── requirements.txt    # Python dependency (psycopg2)
└── README.md

## Requirements

- PostgreSQL (with pgAdmin)
- Python 3.8 or newer
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

## 3. Install Dependencies

From the project root, create a virtual environment:

```sh
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```sh
source .venv/bin/activate
```

Install the PostgreSQL driver:

```sh
python -m pip install -r application/requirements.txt
```

Python is interpreted, so no compilation step is required.
