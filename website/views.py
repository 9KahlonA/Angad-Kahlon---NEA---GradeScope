from flask import Blueprint, render_template, request
from .models import YearGroup, Class, Student  # Assuming these models exist

views = Blueprint('views', __name__)

@views.route('/language')
def language():
    year_groups = YearGroup.query.all()  # Fetch all year groups
    return render_template('language.html', year_groups=year_groups)

@views.route('/literature')
def literature():
    year_groups = YearGroup.query.all()  # Fetch all year groups
    return render_template('literature.html', year_groups=year_groups)

@views.route('/language/<int:year_group_id>')
def language_classes(year_group_id):
    classes = Class.query.filter_by(yeargroup_id=year_group_id).all()  # Correct column name
    return render_template('language_classes.html', classes=classes, year_group_id=year_group_id)

@views.route('/literature/<int:year_group_id>')
def literature_classes(year_group_id):
    classes = Class.query.filter_by(yeargroup_id=year_group_id).all()  # Correct column name
    return render_template('literature_classes.html', classes=classes, year_group_id=year_group_id)

@views.route('/student/<int:student_id>', methods=['GET', 'POST'])  # Allow both GET and POST methods
def student_details(student_id):
    student = Student.query.filter_by(student_id=student_id).first()  # Fetch the student by ID
    if not student:
        return "Student not found", 404

    if request.method == 'POST':
        # Update student details from the form
        student.first_name = request.form.get('first_name')
        student.last_name = request.form.get('last_name')
        student.ethnicity = request.form.get('ethnicity')
        student.home_language = request.form.get('home_language')
        student.reading_age = request.form.get('reading_age')
        db.session.commit()  # Save changes to the database
        return render_template('student_details.html', student=student, success=True)

    # Fetch the class and year group details
    class_info = Class.query.filter_by(class_id=student.class_id).first()
    year_group = (
        YearGroup.query
        .join(Class, YearGroup.yeargroup_id == Class.yeargroup_id)
        .filter(Class.class_id == student.class_id)
        .first()
    )
    return render_template('student_details.html', student=student, class_info=class_info, year_group=year_group)

@views.route('/language/class/<int:class_id>')
def language_class_students(class_id):
    students = Student.query.filter_by(class_id=class_id).with_entities(
        Student.student_id, Student.first_name, Student.last_name, Student.class_id
    ).all()  # Fetch students for the class
    return render_template('class_students.html', subject="Language", students=students)