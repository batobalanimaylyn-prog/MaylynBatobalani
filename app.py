from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# -------------------------
# Student Model
# -------------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(50), nullable=False)


# -------------------------
# Create database + insert sample data
# -------------------------
with app.app_context():
    db.create_all()

    # Insert default students if database is empty
    if Student.query.count() == 0:
        student1 = Student(name="Juan Dela Cruz", grade=10, section="Zechariah")
        student2 = Student(name="Maria Santos", grade=11, section="Genesis")
        student3 = Student(name="Pedro Reyes", grade=12, section="Exodus")

        db.session.add(student1)
        db.session.add(student2)
        db.session.add(student3)
        db.session.commit()


# -------------------------
# Home Route
# -------------------------
@app.route("/")
def home():
    return jsonify({"message": "Student API with database"})


# -------------------------
# Get all students
# -------------------------
@app.route("/students")
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
# Get one student
# -------------------------
@app.route("/students/<int:id>")
def get_student(id):

    student = Student.query.get_or_404(id)

    return jsonify({
        "id": student.id,
        "name": student.name,
        "grade": student.grade,
        "section": student.section
    })


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
