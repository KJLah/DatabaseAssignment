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

## Setup

