"""
utils/db_connection.py
-----------------------
Centralized PostgreSQL connection handler for Cricbuzz LiveStats project.
Uses psycopg2 to connect to the local PostgreSQL database.
"""

import psycopg2
import psycopg2.extras
import streamlit as st

# ─── Database Configuration ───────────────────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "database": "cricbuzz_project",
    "user": "postgres",
    "password": "your_password_here",   # Replace with your actual password
    "port": "5432"
}


def get_connection():
    """
    Establishes and returns a psycopg2 connection to PostgreSQL.
    Returns None if connection fails (with error shown in Streamlit).
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None


def run_query(query: str, params=None):
    """
    Executes a SELECT query and returns results as a list of dicts.
    
    Args:
        query  : SQL SELECT string
        params : Optional tuple of query parameters (for parameterized queries)
    
    Returns:
        list of dict rows, or empty list on failure
    """
    conn = get_connection()
    if conn is None:
        return []
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            results = cur.fetchall()
        conn.close()
        return [dict(row) for row in results]
    except Exception as e:
        st.error(f"❌ Query failed: {e}")
        conn.close()
        return []


def run_write(query: str, params=None):
    """
    Executes an INSERT / UPDATE / DELETE query and commits.
    
    Args:
        query  : SQL write string
        params : Optional tuple of parameters
    
    Returns:
        True on success, False on failure
    """
    conn = get_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"❌ Write failed: {e}")
        conn.rollback()
        conn.close()
        return False
