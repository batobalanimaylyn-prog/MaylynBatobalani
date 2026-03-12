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
    <h1>Welcome to my Flask API!</h1>
    <p>Go to the <a href='/students'>Students Page</a> to view student info.</p>
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
    <h1>Student List</h1>
    <form method="post">
        <label for="student_id">Search by ID:</label>
        <input type="text" name="student_id" id="student_id">
        <button type="submit">Search</button>
    </form>

    {% if search_result %}
        <h2>Search Result:</h2>
        <ul>
            <li>ID: {{ search_result.id }}</li>
            <li>Name: {{ search_result.name }}</li>
            <li>Grade: {{ search_result.grade }}</li>
            <li>Section: {{ search_result.section }}</li>
        </ul>
    {% elif search_result is not none %}
        <p>No student found with that ID.</p>
    {% endif %}

    <h2>All Students:</h2>
    <table border="1" cellpadding="10">
        <tr>
            <th>ID</th><th>Name</th><th>Grade</th><th>Section</th>
        </tr>
        {% for student in students %}
        <tr>
            <td>{{ student.id }}</td>
            <td>{{ student.name }}</td>
            <td>{{ student.grade }}</td>
            <td>{{ student.section }}</td>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html, students=students, search_result=search_result)

if __name__ == "__main__":
    app.run(debug=True)
