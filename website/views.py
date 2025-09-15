from flask import Blueprint, render_template, request, url_for
from .models import YearGroup, Class, Student, Terms, Grades
from . import db
from .Algorithms.fetch_and_predict import fetch_student_for_prediction
from .Algorithms.Prediction_Model import GradePredictor

views = Blueprint('views', __name__)

def get_recent_terms():
    return [term.term_name for term in Terms.query.order_by(Terms.term_id.asc()).limit(4).all()]

def get_student_grades_for_subject(students, terms, subject_id):
    student_grades = {}
    for student in students:
        grades = {}
        for term in terms:
            grade = Grades.query.filter_by(
                student_id=student.student_id, 
                term_id=term.term_id, 
                subject_id=subject_id
            ).first()
            grades[term.term_name] = grade.grade if grade else "N/A"
        student_grades[student.student_id] = grades
    return student_grades

def get_navigation_context(current_route, **kwargs):
    navigation = {
        'show_back': True,
        'back_url': None,
        'back_text': 'Back'
    }
    
    if current_route == 'views.language' or current_route == 'views.literature':
        navigation['back_url'] = 'auth.dashboard'
        navigation['back_text'] = 'Dashboard'
    elif current_route == 'views.language_classes':
        navigation['back_url'] = 'views.language'
        navigation['back_text'] = 'Language'
    elif current_route == 'views.literature_classes':
        navigation['back_url'] = 'views.literature'
        navigation['back_text'] = 'Literature'
    elif current_route == 'views.language_class_students':
        class_id = kwargs.get('class_id')
        if class_id:
            class_obj = Class.query.get(class_id)
            if class_obj:
                navigation['back_url'] = 'views.language_classes'
                navigation['back_params'] = {'year_group_id': class_obj.yeargroup_id}
                navigation['back_text'] = 'Language Classes'
    elif current_route == 'views.literature_class_students':
        class_id = kwargs.get('class_id')
        if class_id:
            class_obj = Class.query.get(class_id)
            if class_obj:
                navigation['back_url'] = 'views.literature_classes'
                navigation['back_params'] = {'year_group_id': class_obj.yeargroup_id}
                navigation['back_text'] = 'Literature Classes'
    elif current_route == 'views.student_details' or current_route == 'views.student_projections':
        student_id = kwargs.get('student_id')
        if student_id:
            from_param = request.args.get('from')
            referrer = request.referrer
            print(f"DEBUG: From param: {from_param}, Referrer: {referrer}")
            
            if from_param == 'search' or (referrer and '/search' in referrer):
                print(f"DEBUG: Detected search source, setting back to search")
                navigation['back_url'] = 'auth.search_page'
                navigation['back_text'] = 'Back to Search'
            else:
                print(f"DEBUG: No search source detected, using default class navigation")
                student = Student.query.get(student_id)
                if student:
                    class_obj = Class.query.get(student.class_id)
                    if class_obj:
                        if 'Language' in class_obj.class_code:
                            navigation['back_url'] = 'views.language_class_students'
                            navigation['back_text'] = 'Language Class'
                        else:
                            navigation['back_url'] = 'views.literature_class_students'
                            navigation['back_text'] = 'Literature Class'
                        navigation['back_params'] = {'class_id': student.class_id}
    elif current_route == 'auth.dashboard':
        navigation['show_back'] = False
    
    return navigation

@views.route('/language')
def language():
    return render_subject_page('language', 'views.language')

@views.route('/literature')
def literature():
    return render_subject_page('literature', 'views.literature')

def render_subject_page(subject, route_name):
    year_groups = YearGroup.query.filter(YearGroup.year != 11).all()
    navigation = get_navigation_context(route_name)
    return render_template(f'{subject}.html', year_groups=year_groups, navigation=navigation)

@views.route('/language/<int:year_group_id>')
def language_classes(year_group_id): 
    return render_classes_page('language', year_group_id, 'views.language_classes')

@views.route('/literature/<int:year_group_id>')
def literature_classes(year_group_id):
    return render_classes_page('literature', year_group_id, 'views.literature_classes')

def render_classes_page(subject, year_group_id, route_name):
    classes = Class.query.filter_by(yeargroup_id=year_group_id).all()
    navigation = get_navigation_context(route_name)
    return render_template(f'{subject}_classes.html', classes=classes, year_group_id=year_group_id, navigation=navigation)

@views.route('/student/<int:student_id>', methods=['GET', 'POST'])
def student_details(student_id): 
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        return "Student not found", 404

    if request.method == 'POST':
        student.first_name = request.form.get('first_name')
        student.last_name = request.form.get('last_name')
        student.ethnicity = request.form.get('ethnicity')
        student.home_language = request.form.get('home_language')
        student.reading_age = request.form.get('reading_age')
        db.session.commit()
        terms_columns = get_recent_terms()
        navigation = get_navigation_context('views.student_details', student_id=student_id)
        return render_template('student_details.html', student=student, terms_columns=terms_columns, success=True, class_id=student.class_id, subject=determine_subject(student.class_id), navigation=navigation)

    class_info = Class.query.filter_by(class_id=student.class_id).first()
    year_group = (
        YearGroup.query
        .join(Class, YearGroup.yeargroup_id == Class.yeargroup_id)
        .filter(Class.class_id == student.class_id)
        .first()
    )
    terms_columns = get_recent_terms()
    navigation = get_navigation_context('views.student_details', student_id=student_id)
    return render_template('student_details.html', student=student, class_info=class_info, year_group=year_group, terms_columns=terms_columns, class_id=student.class_id, subject=determine_subject(student.class_id), navigation=navigation)

def determine_subject(class_id):
    class_info = Class.query.filter_by(class_id=class_id).first()
    if "Literature" in class_info.class_code:
        return "Literature"
    elif "Language" in class_info.class_code:
        return "Language"
    return "Unknown"

@views.route('/student/<int:student_id>/projections')
def student_projections(student_id):
    student_db = Student.query.get(student_id)
    if not student_db:
        return "Student not found", 404

    student_obj, class_code = fetch_student_for_prediction(student_id, db)
    if not student_obj:
        return "Not enough data for projection", 404

    predictor = GradePredictor(student_obj)
    predictor.predict()
    predictor.plot_projections()

    all_projections = predictor.projections
    final_prediction = {subject: grade for subject, grade in predictor.get_predicted_grades().items()}

    navigation = get_navigation_context('views.student_projections', student_id=student_id)
    return render_template(
        'student_projections.html',
        student=student_db,
        projections=all_projections,
        final_prediction=final_prediction,
        class_code=class_code,
        navigation=navigation
    )


@views.route('/language/class/<int:class_id>')
def language_class_students(class_id):
    return render_class_students_page(class_id, 1, "Language", 'views.language_class_students')

@views.route('/literature/class/<int:class_id>')
def literature_class_students(class_id):
    return render_class_students_page(class_id, 2, "Literature", 'views.literature_class_students')

def render_class_students_page(class_id, subject_id, subject_name, route_name):
    students = Student.query.filter_by(class_id=class_id).all()
    terms = Terms.query.order_by(Terms.term_id.asc()).limit(4).all()
    terms_columns = [term.term_name for term in terms]
    student_grades = get_student_grades_for_subject(students, terms, subject_id)
    navigation = get_navigation_context(route_name, class_id=class_id)
    return render_template('class_students.html', subject=subject_name, students=students, terms_columns=terms_columns, student_grades=student_grades, navigation=navigation)

@views.route('/class/<int:class_id>')
def class_page(class_id):
    class_name = Class.query.filter_by(class_id=class_id).first().class_code
    students = Student.query.filter_by(class_id=class_id).all()
    terms_columns = get_recent_terms()
    return render_template('class_page.html', class_name=class_name, students=students, terms_columns=terms_columns)