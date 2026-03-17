from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# -----------------------------
# Database Configuration
# -----------------------------
db = mysql.connector.connect(
    host="sql100.byethost7.com",
    user="b7_41059855",     # replace this
    password="Maylynvila15", # replace this
    database="b7_41059855_student"
)

cursor = db.cursor(dictionary=True)


# -----------------------------
# Home Route
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Student API connected to MySQL",
        "routes": [
            "GET /students",
            "GET /students/<id>",
            "POST /students",
            "PUT /students/<id>",
            "DELETE /students/<id>"
        ]
    })


# -----------------------------
# Get All Students
# -----------------------------
@app.route("/students", methods=["GET"])
def get_students():

    query = "SELECT * FROM students"
    cursor.execute(query)

    students = cursor.fetchall()

    return jsonify(students)


# -----------------------------
# Get One Student
# -----------------------------
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):

    query = "SELECT * FROM students WHERE id=%s"
    cursor.execute(query, (id,))

    student = cursor.fetchone()

    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404


# -----------------------------
# Create Student
# -----------------------------
@app.route("/students", methods=["POST"])
def create_student():

    data = request.get_json()

    name = data.get("name")
    grade = data.get("grade")
    section = data.get("section")

    query = "INSERT INTO students (name, grade, section) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, grade, section))

    db.commit()

    return jsonify({"message": "Student added successfully"})


# -----------------------------
# Update Student
# -----------------------------
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.get_json()

    name = data.get("name")
    grade = data.get("grade")
    section = data.get("section")

    query = "UPDATE students SET name=%s, grade=%s, section=%s WHERE id=%s"
    cursor.execute(query, (name, grade, section, id))

    db.commit()

    return jsonify({"message": "Student updated successfully"})


# -----------------------------
# Delete Student
# -----------------------------
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    query = "DELETE FROM students WHERE id=%s"
    cursor.execute(query, (id,))

    db.commit()

    return jsonify({"message": "Student deleted successfully"})


# -----------------------------
# Run Flask Server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
