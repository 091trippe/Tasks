import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify

app = Flask(__name__)

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
            title VARCHAR(200) NOT NULL,
            description TEXT DEFAULT '',
            done BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    return jsonify({
        "message": "Flask API працює!",
        "status": "OK"
    })

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

    title = data.get("title")
    description = data.get("description", "")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tasks (title, description)
        VALUES (%s, %s)
        RETURNING *
        """,
        (title, description)
    )

    task = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    task = cur.fetchone()

    cur.close()
    conn.close()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task)

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json

    title = data.get("title")
    description = data.get("description")
    done = data.get("done")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks
        SET title=%s,
            description=%s,
            done=%s
        WHERE id=%s
        RETURNING *
        """,
        (title, description, done, task_id)
    )

    task = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task)

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id=%s RETURNING *",
        (task_id,)
    )

    task = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "message": "Task deleted"
    })

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
