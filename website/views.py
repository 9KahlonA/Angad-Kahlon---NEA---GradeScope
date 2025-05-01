from flask import Blueprint, render_template, request
from .models import YearGroup, Class, Student, Terms, Grades  # Ensure Grades is imported
from . import db  # Import the db object

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
        terms_columns = [term.term_name for term in Terms.query.order_by(Terms.term_id.asc()).limit(4).all()]  # Fetch term_name values
        return render_template('student_details.html', student=student, terms_columns=terms_columns, success=True)

    # Fetch the class and year group details
    class_info = Class.query.filter_by(class_id=student.class_id).first()
    year_group = (
        YearGroup.query
        .join(Class, YearGroup.yeargroup_id == Class.yeargroup_id)
        .filter(Class.class_id == student.class_id)
        .first()
    )
    terms_columns = [term.term_name for term in Terms.query.order_by(Terms.term_id.asc()).limit(4).all()]  # Fetch term_name values
    return render_template('student_details.html', student=student, class_info=class_info, year_group=year_group, terms_columns=terms_columns)

@views.route('/language/class/<int:class_id>')
def language_class_students(class_id):
    students = Student.query.filter_by(class_id=class_id).all()  # Fetch students for the class
    terms = Terms.query.order_by(Terms.term_id.asc()).limit(4).all()  # Fetch term_name values
    terms_columns = [term.term_name for term in terms]

    # Fetch grades for each student for each term for the "Language" subject
    student_grades = {}
    for student in students:
        grades = {}
        for term in terms:
            grade = (
                Grades.query.filter_by(student_id=student.student_id, term_id=term.term_id, subject_id=1)  # Assuming subject_id=1 is for "Language"
                .first()
            )
            grades[term.term_name] = grade.grade if grade else "N/A"  # Fetch grade or default to "N/A"
        student_grades[student.student_id] = grades

    return render_template('class_students.html', subject="Language", students=students, terms_columns=terms_columns, student_grades=student_grades)

@views.route('/literature/class/<int:class_id>')
def literature_class_students(class_id):
    students = Student.query.filter_by(class_id=class_id).all()  # Fetch students for the class
    terms = Terms.query.order_by(Terms.term_id.asc()).limit(4).all()  # Fetch term_name values
    terms_columns = [term.term_name for term in terms]

    # Fetch grades for each student for each term for the "Literature" subject
    student_grades = {}
    for student in students:
        grades = {}
        for term in terms:
            grade = (
                Grades.query.filter_by(student_id=student.student_id, term_id=term.term_id, subject_id=2)  # Assuming subject_id=2 is for "Literature"
                .first()
            )
            grades[term.term_name] = grade.grade if grade else "N/A"  # Fetch grade or default to "N/A"
        student_grades[student.student_id] = grades

    return render_template('class_students.html', subject="Literature", students=students, terms_columns=terms_columns, student_grades=student_grades)

@views.route('/class/<int:class_id>')
def class_page(class_id):
    class_name = Class.query.filter_by(class_id=class_id).first().class_name  # Fetch class name
    students = Student.query.filter_by(class_id=class_id).all()  # Fetch students for the class
    terms_columns = [term.term_name for term in Terms.query.order_by(Terms.term_id.asc()).limit(4).all()]  # Fetch term_name values
    return render_template('class_page.html', class_name=class_name, students=students, terms_columns=terms_columns)