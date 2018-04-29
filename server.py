"""
server.py

Created by Stephen Andrews, April 11th, 2018
"""

import sqlite3
from datetime import datetime

from flask import Flask, render_template, request

import config
import db

# Represents the node
KITCHEN_ID = 1
ENTRYWAY_ID = 2
HALLWAY_ID = 3

app = Flask(__name__)
# conn = sqlite3.connect(config.DB_NAME)

@app.route('/')
def index():
    """Main page for viewing room layout."""

    query = """
            SELECT *
            FROM monitor
            limit 30
            """

    with sqlite3.connect(config.DB_NAME) as conn:
        try:
            cur = conn.cursor()
            response = cur.execute(query)
            data = []

            entryway_entered = 0
            hallway_entered = 0
            kitchen_entered = 0

            for item in response:
                rec_id, room_id, breach_time, message = item
                temp_time = breach_time.split(' ')
                breach_date = '{date}'.format(date=temp_time[0])
                breach_time = '{time}'.format(time=temp_time[1].split('.')[0])
                # breach_time = '{date}'.format(date=temp_time[0], time=temp_time[1].split('.')[0])
                data.append({'id': rec_id, 'room_id': room_id, 'breach_date': breach_date, 'breach_time': breach_time, 'message': message})

                if room_id == ENTRYWAY_ID:
                    entryway_entered += 1
                elif room_id == HALLWAY_ID:
                    hallway_entered += 1
                elif room_id == KITCHEN_ID:
                    kitchen_entered += 1

            return render_template('index.html.j2', data=data, entryway=entryway_entered, hallway=hallway_entered, kitchen=kitchen_entered)
        except sqlite3.Error as err:
            print(err)

    return render_template('index.html.j2', data=None)

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
    message = request.form['message']

    # Save record in DB
    query = """
            INSERT INTO monitor (
                room_id,
                breach_time,
                message
            ) VALUES (
                ?,
                ?,
                ?
            );
            """

    with sqlite3.connect(config.DB_NAME) as conn:
        try:
            cur = conn.cursor()
            cur.execute(query, (room_id, breach_time, message))
            conn.commit()

            return 'Inserted record: ({}, {})'.format(room_id, breach_time)
        except sqlite3.Error as err:
            print(err)

    return 'shit'


if __name__ == '__main__':
    app.run(port=8080, debug=True)
    db.setup()
