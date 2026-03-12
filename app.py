from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Sample student data
students = [
    {"id": 1, "name": "Alice", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "Bob", "grade": 11, "section": "Daniel"},
    {"id": 3, "name": "Charlie", "grade": 10, "section": "Zechariah"}
]

# Home route
@app.route('/')
def home():
    return """
    <div class="container mt-5">
        <div class="text-center">
            <h1 class="mb-3">Welcome to the Teacher's Dashboard!</h1>
            <p class="lead">Track and encourage your students with ease.</p>
            <a href='/students' class="btn btn-primary btn-lg mt-3">Go to Students Page</a>
        </div>
    </div>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    """

# API route to get all students
@app.route('/api/students', methods=['GET'])
def api_get_students():
    return jsonify(students)

# API route to get a student by ID
@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

# Web UI route to show all students with search form
@app.route('/students', methods=['GET', 'POST'])
def students_page():
    search_result = None
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        if student_id and student_id.isdigit():
            student_id = int(student_id)
            search_result = next((s for s in students if s["id"] == student_id), None)

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
                <p class="lead text-success">Keep inspiring your students every day!</p>
            </div>

            <div class="card mb-4 shadow-sm p-4">
                <h4>Search for a Student by ID</h4>
                <form method="post" class="row g-3 align-items-center">
                    <div class="col-auto">
                        <input type="text" name="student_id" class="form-control" placeholder="Enter Student ID">
                    </div>
                    <div class="col-auto">
                        <button type="submit" class="btn btn-success">Search</button>
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
                <div class="alert alert-warning">No student found with that ID. Keep encouraging them!</div>
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
    return render_template_string(html, students=students, search_result=search_result)

if __name__ == "__main__":
    app.run(debug=True)
