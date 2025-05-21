from flask import Blueprint, render_template, request  # Import necessary Flask tools
from .models import YearGroup, Class, Student, Terms, Grades  # Import the models to use in the views
from . import db  # Import the db object
from .Algorithms.fetch_and_predict import fetch_student_for_prediction  # Import custom fetch logic for prediction
from .Algorithms.Predition_Model import GradePredictor  # Import the predictor class

views = Blueprint('views', __name__)  # Create a blueprint for the views

@views.route('/language')  # Define the route for the language page
def language():
    year_groups = YearGroup.query.all()  # Fetch all year groups
    return render_template('language.html', year_groups=year_groups)  # Display the language page with the year groups

@views.route('/literature')  # Define the route for the literature page
def literature():
    year_groups = YearGroup.query.all()  # Fetch all year groups
    return render_template('literature.html', year_groups=year_groups)  # Display the literature page with the year groups

@views.route('/language/<int:year_group_id>')  # Define the route for language classes with a specific year group ID
def language_classes(year_group_id): 
    classes = Class.query.filter_by(yeargroup_id=year_group_id).all()  # Fetch classes for the year group
    return render_template('language_classes.html', classes=classes, year_group_id=year_group_id)  # Display the language classes page with the classes and year group ID

@views.route('/literature/<int:year_group_id>')  # Define the route for literature classes with a specific year group ID
def literature_classes(year_group_id):
    classes = Class.query.filter_by(yeargroup_id=year_group_id).all()  # Fetch classes for the year group
    return render_template('literature_classes.html', classes=classes, year_group_id=year_group_id)  # Corrected template name and variable

@views.route('/student/<int:student_id>', methods=['GET', 'POST'])  # Define the route for student details with a specific student ID
# The GET and POST Methods are called here to allow displaying and updates to the students table in the db
def student_details(student_id): 
    student = Student.query.filter_by(student_id=student_id).first()  # Fetch the student by ID
    if not student:
        return "Student not found", 404  # Checks if the student exists

    if request.method == 'POST':  # Check if method is POST 
        # Update student details from the form
        student.first_name = request.form.get('first_name')  # Get the first name from the the student details form
        student.last_name = request.form.get('last_name')  # Get the last name from the student details form
        student.ethnicity = request.form.get('ethnicity')  # Get the ehtnivcity from the student details form
        student.home_language = request.form.get('home_language')  # Get the home language from the student details form
        student.reading_age = request.form.get('reading_age')  # Get the reading age from the student details form
        db.session.commit()  # Saves changes to the db
        terms_columns = [term.term_name for term in Terms.query.order_by(Terms.term_id.asc()).limit(4).all()]  # Corrected term_id
        return render_template('student_details.html', student=student, terms_columns=terms_columns, success=True, class_id=student.class_id, subject=determine_subject(student.class_id))  # Pass class_id and subject to the template

    class_info = Class.query.filter_by(class_id=student.class_id).first()  # Fetch the class information for the student
    year_group = (
        YearGroup.query  # Fetch the corresponding year group for the student
        .join(Class, YearGroup.yeargroup_id == Class.yeargroup_id)  # Joins the YearGroup and Class tables
        .filter(Class.class_id == student.class_id)  # Filters the classes by the student class_id
        .first()
    )
    terms_columns = [term.term_name for term in Terms.query.order_by(Terms.term_id.asc()).limit(4).all()]  # Corrected term_id
    return render_template('student_details.html', student=student, class_info=class_info, year_group=year_group, terms_columns=terms_columns, class_id=student.class_id, subject=determine_subject(student.class_id))  # Pass class_id and subject to the template

def determine_subject(class_id):  # Helper function to determine the subject based on the class Id
    class_info = Class.query.filter_by(class_id=class_id).first()
    if "Literature" in class_info.class_code:  # Example logic based on class name
        return "Literature"
    elif "Language" in class_info.class_code:
        return "Language"
    return "Unknown"

@views.route('/student/<int:student_id>/projections')  # Define the route for student projections
def student_projections(student_id):
    student_db = Student.query.get(student_id)  # Fetch the student by ID
    if not student_db:
        return "Student not found", 404  # Return 404 if the student does not exist

    # Use fetch logic to prepare data for predictions
    student_obj, class_code = fetch_student_for_prediction(student_id, db)
    if not student_obj:
        return "Not enough data for projection", 404  # If no grades or subject data

    # Create predictor and run predictions
    predictor = GradePredictor(student_obj)
    predictor.predict()
    predictor.plot_projections()  # Generate and save the graph image

    all_projections = predictor.projections  # Dictionary of year-by-year subject grades
    final_prediction = {subject: grade for subject, grade in predictor.get_predicted_grades().items()}  # Adjusted to handle string keys

    return render_template(
        'student_projections.html',
        student=student_db,
        projections=all_projections,
        final_prediction=final_prediction,  # Adjusted to handle string keys
        class_code=class_code
    )

@views.route('/language/class/<int:class_id>')  # Define the route for language class students with a specific class ID
def language_class_students(class_id):
    students = Student.query.filter_by(class_id=class_id).all()  # Fetch students for the class
    terms = Terms.query.order_by(Terms.term_id.asc()).limit(4).all()  # Corrected term_id
    terms_columns = [term.term_name for term in terms]  # Fetch the term names to use as column names

    # Fetch grades for each student for each term for the "Language" subject
    student_grades = {}
    for student in students:
        grades = {}
        for term in terms:
            grade = (
                Grades.query.filter_by(student_id=student.student_id, term_id=term.term_id, subject_id=1)  # Corrected subject_id
                .first()
            )
            grades[term.term_name] = grade.grade if grade else "N/A"  # Fetch grade or default to "N/A"
        student_grades[student.student_id] = grades

    return render_template('class_students.html', subject="Language", students=students, terms_columns=terms_columns, student_grades=student_grades)

@views.route('/literature/class/<int:class_id>')  # Define the route for literature class students with a specific class ID
def literature_class_students(class_id):
    students = Student.query.filter_by(class_id=class_id).all()  # Fetch students for the class
    terms = Terms.query.order_by(Terms.term_id.asc()).limit(4).all()  # Corrected term_id
    terms_columns = [term.term_name for term in terms]

    # This iterates through a list of students fetched from the db and then iterates through the terms to get the grades for each student in the class for that specific term
    student_grades = {}  # Creates a dictionary of students and their grades for each term
    for student in students:
        grades = {}  # Creates a dictionary of grades for each student
        for term in terms:
            grade = (
                Grades.query.filter_by(student_id=student.student_id, term_id=term.term_id, subject_id=2)  # Corrected subject_id
                .first() 
            )
            grades[term.term_name] = grade.grade if grade else "N/A"  # Fetches the grade for the student in that term or defaults to "N/A" if no grade is found
        student_grades[student.student_id] = grades  # Adds the grades to the student_grades dictionary

    return render_template('class_students.html', subject="Literature", students=students, terms_columns=terms_columns, student_grades=student_grades)  # Returns the class students page with the subject, students, term columns and student grades

@views.route('/class/<int:class_id>')  # Define the route for class page with a specific class ID
def class_page(class_id):
    class_name = Class.query.filter_by(class_id=class_id).first().class_code  # Fetch class name
    students = Student.query.filter_by(class_id=class_id).all()  # Fetch students for the class
    terms_columns = [term.term_name for term in Terms.query.order_by(Terms.term_id.asc()).limit(4).all()]  # Corrected term_id
    return render_template('class_page.html', class_name=class_name, students=students, terms_columns=terms_columns)  # Returns the class page with the class name, students and term columns