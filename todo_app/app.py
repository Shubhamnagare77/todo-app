"""
app.py
------
Main Flask application for the To-Do List app.

Routes:
    GET  /                -> Show all tasks
    POST /add              -> Add a new task
    POST /complete/<id>    -> Toggle a task's completed status
    POST /delete/<id>      -> Delete a task
"""

import logging
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

from database.db import get_connection, init_db

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "todo_app.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Secret key is required for flash messages (used to show errors to the user)
app.secret_key = "dev-secret-key-change-this-in-production"


@app.route("/")
def index():
    """Fetch all tasks from the database and render them on the homepage."""
    try:
        conn = get_connection()
        tasks = conn.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC"
        ).fetchall()
        conn.close()
        logger.info("Loaded %d tasks", len(tasks))
    except sqlite3.Error as e:
        logger.exception("Error loading tasks")
        flash(f"Error loading tasks: {e}", "danger")
        tasks = []

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    """Add a new task to the database."""
    title = request.form.get("title", "").strip()

    # Basic validation - don't allow empty tasks
    if not title:
        logger.warning("Attempted to add empty task title")
        flash("Task title cannot be empty.", "warning")
        return redirect(url_for("index"))

    try:
        conn = get_connection()
        conn.execute("INSERT INTO tasks (title, completed) VALUES (?, 0)", (title,))
        conn.commit()
        conn.close()
        logger.info("Added task: %s", title)
        flash("Task added successfully.", "success")
    except sqlite3.Error as e:
        logger.exception("Error adding task")
        flash(f"Error adding task: {e}", "danger")

    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    """Toggle a task's completed status (done <-> not done)."""
    try:
        conn = get_connection()
        task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

        if task is None:
            logger.warning("Attempted to complete unknown task id=%d", task_id)
            flash("Task not found.", "warning")
        else:
            new_status = 0 if task["completed"] else 1
            conn.execute(
                "UPDATE tasks SET completed = ? WHERE id = ?", (new_status, task_id)
            )
            conn.commit()
            logger.info(
                "Updated task id=%d completed=%s", task_id, bool(new_status)
            )

        conn.close()
    except sqlite3.Error as e:
        logger.exception("Error updating task id=%d", task_id)
        flash(f"Error updating task: {e}", "danger")

    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """Delete a task from the database."""
    try:
        conn = get_connection()
        result = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

        if result.rowcount == 0:
            logger.warning("Attempted to delete unknown task id=%d", task_id)
            flash("Task not found.", "warning")
        else:
            logger.info("Deleted task id=%d", task_id)
            flash("Task deleted.", "info")
    except sqlite3.Error as e:
        logger.exception("Error deleting task id=%d", task_id)
        flash(f"Error deleting task: {e}", "danger")

    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 handler so users don't see a raw stack trace."""
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Ensure the database and table exist before the app starts handling requests
    logger.info("Starting To-Do app")
    init_db()
    app.run(debug=True)
