"""
db.py

Created by Stephen Andrews, April 11th, 2018.
"""

import sqlite3

import config

conn = sqlite3.connect(config.DB_NAME)

def setup():
    """Setup the required tables."""

    query = """
            CREATE TABLE monitor (
                id integer primary key,
                room_id integer,
                breach_time timestamp
            );
            """

    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

    return cur.rowcount > 0
