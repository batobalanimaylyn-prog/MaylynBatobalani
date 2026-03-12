from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Sample student data
students = [
    {"id": 1, "name": "Alice", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "Bob", "grade": 11, "section": "Daniel"},
    {"id": 3, "name": "Charlie", "grade": 10, "section": "Zechariah"}
]

# Helper to generate new ID
def next_id():
    return max([s["id"] for s in students], default=0) + 1

# Home page
@app.route('/')
def home():
    return """
    <div class="container mt-5">
        <div class="text-center">
            <h1 class="mb-3">Welcome to the Teacher's Dashboard!</h1>
            <p class="lead">Manage and encourage your students effectively.</p>
            <a href='/students' class="btn btn-primary btn-lg mt-3">Go to Students Page</a>
        </div>
    </div>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    """

# API Routes
@app.route('/api/students', methods=['GET'])
def api_get_students():
    return jsonify(students)

@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    return jsonify(student) if student else (jsonify({"error": "Student not found"}), 404)

@app.route('/api/students', methods=['POST'])
def api_create_student():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "grade", "section")):
        return jsonify({"error": "Invalid data"}), 400
    new_student = {
        "id": next_id(),
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }
    students.append(new_student)
    return jsonify(new_student), 201

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def api_update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    data = request.get_json() or {}
    student.update({
        "name": data.get("name", student["name"]),
        "grade": data.get("grade", student["grade"]),
        "section": data.get("section", student["section"])
    })
    return jsonify(student)

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    global students
    if any(s["id"] == student_id for s in students):
        students = [s for s in students if s["id"] != student_id]
        return jsonify({"message": "Student deleted successfully"})
    return jsonify({"error": "Student not found"}), 404

# Web UI for CRUD operations
@app.route('/students', methods=['GET', 'POST'])
def students_page():
    message = None
    search_result = None

    if request.method == 'POST':
        action = request.form.get("action")
        student_id = request.form.get("student_id")
        name = request.form.get("name", "").strip()
        grade = request.form.get("grade", "").strip()
        section = request.form.get("section", "").strip()

        # Convert ID safely
        student_id_int = int(student_id) if student_id and student_id.isdigit() else None
        grade_int = int(grade) if grade.isdigit() else None

        if action == "search" and student_id_int:
            search_result = next((s for s in students if s["id"] == student_id_int), None)
        elif action == "add" and name and grade_int is not None and section:
            new_student = {"id": next_id(), "name": name, "grade": grade_int, "section": section}
            students.append(new_student)
            message = {"type": "success", "text": f"Student {name} added successfully!"}
        elif action == "update" and student_id_int:
            student = next((s for s in students if s["id"] == student_id_int), None)
            if student:
                student.update({
                    "name": name or student["name"],
                    "grade": grade_int if grade else student["grade"],
                    "section": section or student["section"]
                })
                message = {"type": "success", "text": f"Student {student['name']} updated successfully!"}
            else:
                message = {"type": "danger", "text": "Student not found."}
        elif action == "delete" and student_id_int:
            if any(s["id"] == student_id_int for s in students):
                students[:] = [s for s in students if s["id"] != student_id_int]
                message = {"type": "success", "text": "Student deleted successfully."}
            else:
                message = {"type": "danger", "text": "Student not found."}

    # Render HTML
    html = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Student Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container py-5">
            <div class="text-center mb-4">
                <h1 class="display-5">Student Dashboard</h1>
                <p class="lead text-success">Manage your students and celebrate their progress!</p>
            </div>

            {% if message %}
                <div class="alert alert-{{ message.type }}">{{ message.text }}</div>
            {% endif %}

            <div class="card mb-4 shadow-sm p-4">
                <h4 class="mb-3">CRUD Operations</h4>
                <form method="post" class="row g-3">
                    <div class="col-md-2">
                        <input type="text" name="student_id" class="form-control" placeholder="ID">
                    </div>
                    <div class="col-md-3">
                        <input type="text" name="name" class="form-control" placeholder="Name">
                    </div>
                    <div class="col-md-2">
                        <input type="text" name="grade" class="form-control" placeholder="Grade">
                    </div>
                    <div class="col-md-2">
                        <input type="text" name="section" class="form-control" placeholder="Section">
                    </div>
                    <div class="col-md-3 d-flex flex-wrap gap-2">
                        <button type="submit" name="action" value="add" class="btn btn-success">Add</button>
                        <button type="submit" name="action" value="update" class="btn btn-primary">Update</button>
                        <button type="submit" name="action" value="delete" class="btn btn-danger">Delete</button>
                        <button type="submit" name="action" value="search" class="btn btn-info">Search</button>
                    </div>
                </form>
            </div>

            {% if search_result %}
                <div class="card mb-4 shadow-sm p-3 border-success">
                    <h5 class="text-success">🎉 Student Found!</h5>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item"><strong>ID:</strong> {{ search_result.id }}</li>
                        <li class="list-group-item"><strong>Name:</strong> {{ search_result.name }}</li>
                        <li class="list-group-item"><strong>Grade:</strong> {{ search_result.grade }}</li>
                        <li class="list-group-item"><strong>Section:</strong> {{ search_result.section }}</li>
                    </ul>
                </div>
            {% elif search_result is not none %}
                <div class="alert alert-warning">No student found with that ID.</div>
            {% endif %}

            <div class="card shadow-sm p-3">
                <h4 class="mb-3">All Students</h4>
                <table class="table table-striped table-hover">
                    <thead class="table-success">
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Grade</th>
                            <th>Section</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for student in students %}
                        <tr>
                            <td>{{ student.id }}</td>
                            <td>{{ student.name }}</td>
                            <td>{{ student.grade }}</td>
                            <td>{{ student.section }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>

            <footer class="text-center mt-5">
                <p class="text-muted">💡 Remember: Every student can shine with your guidance!</p>
            </footer>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, students=students, search_result=search_result, message=message)

if __name__ == "__main__":
    app.run(debug=True)
