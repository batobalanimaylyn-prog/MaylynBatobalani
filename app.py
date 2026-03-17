in action add update button
from flask import Flask, request, render_template_string, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"  # change this in production

# -----------------------------
# DATABASE
# -----------------------------
def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    # Students table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        grade INTEGER,
        section TEXT
    )
    """)

    # Users table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Default teacher account
    conn.execute("""
    INSERT OR IGNORE INTO users (id, username, password)
    VALUES (1, 'teacher', 'password123')
    """)

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# LOGIN REQUIRED DECORATOR
# -----------------------------
def login_required(func):
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# -----------------------------
# LOGIN PAGE
# -----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect(url_for("students_page"))
        else:
            message = "Invalid credentials"

    return render_template_string("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <div class="container mt-5 col-md-4">
        <h2 class="mb-3 text-center">Teacher Login</h2>

        {% if message %}
            <div class="alert alert-danger">{{ message }}</div>
        {% endif %}

        <form method="post">
            <input class="form-control mb-2" name="username" placeholder="Username" required>
            <input type="password" class="form-control mb-2" name="password" placeholder="Password" required>
            <button class="btn btn-primary w-100">Login</button>
        </form>
    </div>
    """, message=message)

# -----------------------------
# LOGOUT
# -----------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

# -----------------------------
# HOME
# -----------------------------
@app.route('/')
def home():
    return redirect(url_for("login"))

# -----------------------------
# STUDENTS PAGE (PROTECTED)
# -----------------------------
@app.route('/students', methods=['GET', 'POST'])
@login_required
def students_page():
    conn = get_db()
    message = None

    if request.method == 'POST':
        action = request.form.get("action")
        name = request.form.get("name")
        grade = request.form.get("grade")
        section = request.form.get("section")
        student_id = request.form.get("student_id")

        if action == "add":
            conn.execute("INSERT INTO students (name, grade, section) VALUES (?, ?, ?)",
                         (name, grade, section))
            conn.commit()
            message = "Student added!"

        elif action == "delete":
            conn.execute("DELETE FROM students WHERE id=?", (student_id,))
            conn.commit()
            message = "Deleted!"

    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return render_template_string("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

    <div class="container mt-4">
        <div class="d-flex justify-content-between">
            <h2>Student Dashboard</h2>
            <a href="/logout" class="btn btn-danger">Logout</a>
        </div>

        {% if message %}
            <div class="alert alert-success mt-2">{{ message }}</div>
        {% endif %}

        <form method="post" class="row g-2 mt-3">
            <input class="form-control col" name="name" placeholder="Name">
            <input class="form-control col" name="grade" placeholder="Grade">
            <input class="form-control col" name="section" placeholder="Section">

            <button name="action" value="add" class="btn btn-success mt-2">Add</button>
        </form>

        <table class="table mt-4">
            <tr><th>ID</th><th>Name</th><th>Grade</th><th>Section</th><th>Action</th></tr>
            {% for s in students %}
            <tr>
                <td>{{ s.id }}</td>
                <td>{{ s.name }}</td>
                <td>{{ s.grade }}</td>
                <td>{{ s.section }}</td>
                <td>
                    <form method="post">
                        <input type="hidden" name="student_id" value="{{ s.id }}">
                        <button name="action" value="delete" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
    """, students=students, message=message)

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
