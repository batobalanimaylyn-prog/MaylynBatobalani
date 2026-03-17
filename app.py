from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///students.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(50), nullable=False)


# Create database tables
with app.app_context():
    db.create_all()


# Home Route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Flask CRUD API"})


# CREATE Student
@app.route("/students", methods=["POST"])
def create_student():
    data = request.json

    student = Student(
        name=data["name"],
        grade=data["grade"],
        section=data["section"]
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student created successfully"})


# READ All Students
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


# READ One Student
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    student = Student.query.get_or_404(id)

    return jsonify({
        "id": student.id,
        "name": student.name,
        "grade": student.grade,
        "section": student.section
    })


# UPDATE Student
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.json

    student.name = data["name"]
    student.grade = data["grade"]
    student.section = data["section"]

    db.session.commit()

    return jsonify({"message": "Student updated successfully"})


# DELETE Student
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
