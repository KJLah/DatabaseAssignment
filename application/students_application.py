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