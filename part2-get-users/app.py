#!/usr/bin/python
import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def connect_to_db():
    return sqlite3.connect('database.db')


def create_db_table():
    conn = connect_to_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()


def get_user_names():
    conn = connect_to_db()
    try:
        rows = conn.execute("SELECT name FROM users").fetchall()
        return [row[0] for row in rows]
    finally:
        conn.close()


# GET: list of the names of all users in the database
@app.route("/get_users", methods=["GET"])
def api_get_users():
    return jsonify(get_user_names())


if __name__ == "__main__":
    create_db_table()
    # host="0.0.0.0" so the API is reachable from outside the Docker container
    app.run(host="0.0.0.0", port=3000, debug=True)
