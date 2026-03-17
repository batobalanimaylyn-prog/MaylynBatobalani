# app.py
from flask import Flask, request, render_template_string, redirect, url_for, session
import pymysql
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallbacksecret")

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db():
    return pymysql.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        database=os.environ.get("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        grade INT NOT NULL,
        section VARCHAR(50) NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(50) NOT NULL
    )
    """)
    cursor.execute("""
    INSERT IGNORE INTO users (id, username, password)
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
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session["user"] = username
            return redirect(url_for("students_page"))
        else:
            message = "Invalid credentials"

    return render_template_string("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <div class="container mt-5 col-md-4">
        <h2 class="text-center">Teacher Login</h2>
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
# STUDENTS DASHBOARD
# -----------------------------
@app.route('/students', methods=['GET', 'POST'])
@login_required
def students_page():
    conn = get_db()
    cursor = conn.cursor()
    message = None
    search_result = None

    if request.method == 'POST':
        action = request.form.get("action")
        student_id = request.form.get("student_id")
        name = request.form.get("name")
        grade = request.form.get("grade")
        section = request.form.get("section")

        # Convert student_id and grade to int safely
        student_id_int = int(student_id) if student_id and student_id.isdigit() else None
        grade_int = int(grade) if grade and grade.isdigit() else None

        if action == "add" and name and grade_int and section:
            cursor.execute("INSERT INTO students (name, grade, section) VALUES (%s, %s, %s)", (name, grade_int, section))
            conn.commit()
            message = "Student added!"

        elif action == "delete" and student_id_int:
            cursor.execute("DELETE FROM students WHERE id=%s", (student_id_int,))
            conn.commit()
            message = "Student deleted!"

        elif action == "search" and student_id_int:
            cursor.execute("SELECT * FROM students WHERE id=%s", (student_id_int,))
            search_result = cursor.fetchone()
            message = f"Found: {search_result['name']}" if search_result else "Student not found"

        elif action == "edit" and student_id_int and (name or grade_int or section):
            cursor.execute("SELECT * FROM students WHERE id=%s", (student_id_int,))
            student = cursor.fetchone()
            if student:
                new_name = name if name else student['name']
                new_grade = grade_int if grade_int else student['grade']
                new_section = section if section else student['section']
                cursor.execute("UPDATE students SET name=%s, grade=%s, section=%s WHERE id=%s", (new_name, new_grade, new_section, student_id_int))
                conn.commit()
                message = "Student updated!"
            else:
                message = "Student not found"

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()

    return render_template_string("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #ff9a9e, #fad0c4); min-height: 100vh; }
        .card { border-radius: 15px; }
    </style>
    <div class="container mt-4">
        <div class="d-flex justify-content-between text-white">
            <h2>🌸 Student Dashboard</h2>
            <a href="/logout" class="btn btn-dark">Logout</a>
        </div>
        {% if message %}
            <div class="alert alert-light mt-3">{{ message }}</div>
        {% endif %}

        <!-- FORM -->
        <div class="card p-4 mt-3 shadow">
            <form method="post" class="row g-2">
                <input class="form-control col" name="student_id" placeholder="Student ID (for search/edit)">
                <input class="form-control col" name="name" placeholder="Name">
                <input class="form-control col" name="grade" placeholder="Grade">
                <input class="form-control col" name="section" placeholder="Section">
                <div class="mt-2">
                    <button name="action" value="add" class="btn btn-success">Add</button>
                    <button name="action" value="search" class="btn btn-primary">Search</button>
                    <button name="action" value="edit" class="btn btn-warning">Edit</button>
                </div>
            </form>
        </div>

        <!-- SEARCH RESULT -->
        {% if search_result %}
            <div class="card mt-3 p-3 shadow border-success">
                <h5>🎉 Student Found!</h5>
                <p><strong>ID:</strong> {{ search_result.id }}</p>
                <p><strong>Name:</strong> {{ search_result.name }}</p>
                <p><strong>Grade:</strong> {{ search_result.grade }}</p>
                <p><strong>Section:</strong> {{ search_result.section }}</p>
            </div>
        {% endif %}

        <!-- STUDENT TABLE -->
        <div class="card mt-4 p-3 shadow">
            <table class="table table-hover">
                <tr><th>ID</th><th>Name</th><th>Grade</th><th>Section</th><th>Action</th></tr>
                {% for s in students %}
                <tr>
                    <td>{{ s.id }}</td>
                    <td>{{ s.name }}</td>
                    <td>{{ s.grade }}</td>
                    <td>{{ s.section }}</td>
                    <td>
                        <form method="post" style="display:inline;">
                            <input type="hidden" name="student_id" value="{{ s.id }}">
                            <button name="action" value="delete" class="btn btn-danger btn-sm">Delete</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </div>
    """, students=students, message=message, search_result=search_result)

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
