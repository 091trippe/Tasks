import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

def get_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        cursor_factory=RealDictCursor
    )

def init_db():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            done BOOLEAN DEFAULT FALSE
        )
    """)

    conn.commit()

    cur.close()
    conn.close()

@app.route("/tasks", methods=["GET"])
def get_tasks():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks ORDER BY id")

    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def create_task():

    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tasks (title)
        VALUES (%s)
        RETURNING *
        """,
        (data["title"],)
    )

    task = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    return jsonify(task)

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):

    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks
        SET done=%s
        WHERE id=%s
        RETURNING *
        """,
        (data["done"], id)
    )

    task = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    return jsonify(task)

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id=%s",
        (id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "message": "Task deleted"
    })

if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000
    )
