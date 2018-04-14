"""
server.py

Created by Stephen Andrews, April 11th, 2018
"""

import sqlite3

from flask import Flask, render_template, request

import config
import db


app = Flask(__name__)
# conn = sqlite3.connect(config.DB_NAME)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/<room_id>/<time>")
def hello(room_id, time):
    return "{} {}".format(room_id, time)

@app.route('/api/', methods=['POST'])
def api():
    """API endpoint to receive transmission data from a node."""

    if not request.form:
        return "Invalid request", 500

    room_id = request.form['room_id']
    breach_time = request.form['breach_time']

    # Save record in DB
    query = """
            INSERT INTO monitor (
                room_id,
                breach_time
            ) VALUES (
                ?,
                ?
            );
            """

    with sqlite3.connect(config.DB_NAME) as conn:
        try:
            cur = conn.cursor()
            cur.execute(query, (room_id, breach_time))
            conn.commit()

            return 'Inserted record: ({}, {})'.format(room_id, breach_time)
        except sqlite3.Error as err:
            print(err)

    return 'shit'


if __name__ == '__main__':
    app.run(port=8080, debug=True)
    db.setup()
