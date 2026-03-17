from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    grade = db.Column(db.Integer)
    section = db.Column(db.String(50))

# Create database
with app.app_context():
    db.create_all()


# Home route
@app.route('/')
def home():
    return "Welcome to my Flask CRUD API!"


# CREATE student
@app.route('/student', methods=['POST'])
def create_student():
    data = request.json

    new_student = Student(
        name=data['name'],
        grade=data['grade'],
        section=data['section']
    )

    db.session.add(new_student)
    db.session.commit()

    return jsonify({"message": "Student added successfully"})


# READ all students
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()

    output = []

    for student in students:
        student_data = {
            "id": student.id,
            "name": student.name,
            "grade": student.grade,
            "section": student.section
        }
        output.append(student_data)

    return jsonify(output)


# READ one student
@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)

    return jsonify({
        "id": student.id,
        "name": student.name,
        "grade": student.grade,
        "section": student.section
    })


# UPDATE student
@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.json

    student.name = data['name']
    student.grade = data['grade']
    student.section = data['section']

    db.session.commit()

    return jsonify({"message": "Student updated successfully"})


# DELETE student
@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
