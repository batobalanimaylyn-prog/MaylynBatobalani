from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
database_url = os.environ.get("DATABASE_URL")

if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# -------------------------
# Database Model
# -------------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(50), nullable=False)


# Create database automatically
with app.app_context():
    db.create_all()


# -------------------------
# Home Route
# -------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Flask CRUD API is running",
        "endpoints": [
            "GET /students",
            "GET /students/<id>",
            "POST /students",
            "PUT /students/<id>",
            "DELETE /students/<id>"
        ]
    })


# -------------------------
# CREATE Student
# -------------------------
@app.route("/students", methods=["POST"])
def create_student():

    data = request.get_json(silent=True) or request.form

    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name")
    grade = data.get("grade")
    section = data.get("section")

    if not name or not grade or not section:
        return jsonify({"error": "Missing required fields"}), 400

    student = Student(
        name=name,
        grade=grade,
        section=section
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student created successfully",
        "student_id": student.id
    })


# -------------------------
# READ All Students
# -------------------------
@app.route("/students", methods=["GET"])
def get_students():

    students = Student.query.all()

    result = []

    for student in students:
        result.append({
            "id": student.id,
            "name": student.name,
            "grade": student.grade,
            "section": student.section
        })

    return jsonify(result)


# -------------------------
# READ One Student
# -------------------------
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):

    student = Student.query.get_or_404(id)

    return jsonify({
        "id": student.id,
        "name": student.name,
        "grade": student.grade,
        "section": student.section
    })


# -------------------------
# UPDATE Student
# -------------------------
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):

    student = Student.query.get_or_404(id)

    data = request.get_json(silent=True) or request.form

    if not data:
        return jsonify({"error": "No data provided"}), 400

    student.name = data.get("name", student.name)
    student.grade = data.get("grade", student.grade)
    student.section = data.get("section", student.section)

    db.session.commit()

    return jsonify({"message": "Student updated successfully"})


# -------------------------
# DELETE Student
# -------------------------
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student deleted successfully"})


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
