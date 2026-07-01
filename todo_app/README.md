# 📝 Flask To-Do List App

A simple, clean To-Do List web application built with **Python**, **Flask**, **SQLite**, and **Bootstrap**.

## Features

- Add new tasks
- Mark tasks as completed / not completed
- Delete tasks
- View all tasks, persisted in a SQLite database
- Responsive UI using Bootstrap
- Basic error handling and user feedback (flash messages)

## Project Structure

```
todo_app/
├── app.py                 # Main Flask application (routes/CRUD logic)
├── requirements.txt        # Python dependencies
├── database/
│   ├── __init__.py
│   ├── db.py               # Database connection & schema setup
│   └── todo.db              # SQLite database file (auto-created on first run)
├── templates/
│   ├── index.html           # Main page template
│   └── 404.html              # Custom "not found" page
└── static/
    ├── css/
    │   └── style.css         # Custom styling
    └── js/
        └── script.js          # Small UX enhancements (auto-dismiss alerts)
```

## Requirements

- Python 3.8+
- pip

## Setup Instructions

1. **Clone or download** this project folder to your machine.

2. **(Recommended) Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   python app.py
   ```

   On first run, `app.py` automatically creates the SQLite database
   (`database/todo.db`) and the `tasks` table if they don't already exist.

5. **Open your browser** and go to:

   ```
   http://127.0.0.1:5000/
   ```

## Usage

- Type a task into the input box and click **Add Task**.
- Click the checkbox icon (⬜/✅) next to a task to toggle it as completed.
- Click the trash icon (🗑️) to delete a task.
- Any errors (e.g., database issues, empty input) are shown as dismissible
  alert banners at the top of the page.

## Notes on Configuration

- The Flask app runs in `debug=True` mode by default for easier local
  development. **Turn this off (`debug=False`) before deploying to
  production**, and set a strong, random `app.secret_key` via an environment
  variable instead of the hardcoded placeholder in `app.py`.
- The database file lives at `database/todo.db`. Delete this file if you
  want to reset all tasks (it will be recreated automatically on next run).

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite (via Python's built-in `sqlite3` module)
- **Frontend:** HTML, CSS, Bootstrap 5
- **Templating:** Jinja2 (bundled with Flask)

Training: Added by shubham on feature branch.
