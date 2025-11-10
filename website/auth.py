from flask import Blueprint,render_template,request , redirect, url_for,flash, jsonify, session
from . models import User,Student,Class , YearGroup,Grades, Terms
from sqlalchemy import or_,and_
from functools import wraps
auth = Blueprint('auth' , __name__)

# Condition to ensure login is required to access any pages. 
# Maps the user_id to a session and only then can the site be accessed
def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', category='error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Checks which user is currently logged in
def get_current_user():
    """Get the current logged-in user"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

# Route relating to logging in, and managing sessions
@auth.route('/login', methods=['GET', 'POST']) 
def login():
    # If already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('auth.dashboard'))
    
    if request. method == 'POST':
        username = request .form.get('username')
        password = request. form.get('password')
        user = User. query .filter_by(username=username). first()
        if user and user. check_password(password):
            session['user_id'] = user.id
            flash('Login successful!', category='success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Incorrect username or password', category='error')
    return render_template('login.html')

# Route deefining the logging out process
@auth.route('/logout')
def logout():
    """Logout the current user"""
    session.clear()
    flash('You have been logged out', category='info')
    return redirect(url_for('auth.login'))

# Route defining the dashboard
@auth.route('/dashboard')
@login_required
def dashboard():
    navigation = {'show_back': False}
    return render_template('dashboard.html', navigation=navigation)

# Route defing the studen search function
@auth.route('/search')
@login_required
def search_page():
    navigation = {
        'show_back': True,
        'back_url': 'auth.dashboard',
        'back_text': 'Dashboard'
    }
    return render_template('student_search.html', navigation=navigation)


# API endpoint for the student search functionality
# This will validate inputs and returns JSON errors if invalid
@auth.route('/search_students', methods=['GET', 'POST'])
@login_required
def search_students():
    if request . method == 'POST':
        first_name = request. form. get('first_name', ''). strip()
        last_name = request .form .get('last_name', ''). strip()
        year_group = request. form .get('year_group', '').strip()
        
        if not first_name and not last_name and not year_group:
            return jsonify ({'error': 'Please enter at least one search criteria'}),400
        
        first_name = sanitize_search_input (first_name) if first_name else ''
        last_name = sanitize_search_input(last_name) if last_name else ''
        year_group = sanitize_search_input (year_group) if year_group else ''
        
        # Input validation for length, data type and range of data
        if first_name and (len(first_name) <2 or len(first_name) > 50):
            return jsonify({'error': 'First name must be 2-50 characters long'}), 400
        if first_name and not first_name.isalpha():
            return jsonify({'error': 'First name must only contain letters (a-z, A-Z)'}), 400
        if last_name and (len(last_name) <2 or len(last_name) >50):
            return jsonify({'error':'Last name must be 2-50 characters long'}),400
        if last_name and not last_name.isalpha():
            return jsonify({'error': 'Last name must only contain letters (a-z, A-Z)'}), 400
        if year_group and not year_group. isdigit():
            return jsonify({'error':'Year group must be a number'}),400
        if year_group and (int(year_group) <7 or int(year_group)> 11):
            return jsonify({'error': 'Year group must be between 7 and 11'}), 400
        
        try:
            results = perform_advanced_student_search(first_name, last_name, year_group)
            return jsonify({'results': results})
            # exception handling for errors during a search
        except Exception as e:
            return jsonify({'error' :f'Search failed:{str(e) }'}), 500
    
    return jsonify({'error' :'Invalid request method'}),405

# This section removes specific characters from search queries, prventing SQL Injections
def sanitize_search_input (query ):
    import html
    import re
    
    query = html. escape( query)
    
    dangerous_chars = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_', 'DROP', 'DELETE', 'INSERT', 'UPDATE']
    for char in dangerous_chars:
        query = query.replace(char, '')
    
    query = ' '.join(query.split())
    
    return query

# Performs database search with filters for first name, last name, and year group
def perform_advanced_student_search(first_name, last_name, year_group):
    results = []
    
    query_filters = []
    
    if first_name:
        query_filters.append(Student.first_name.ilike(f'%{first_name}%'))
    
    if last_name:
        query_filters.append(Student.last_name.ilike(f'%{last_name}%'))
    
    if year_group:
        year_num = int(year_group)
        # Match year group by exact year value (stored as integer in database)
        year_groups = YearGroup.query.filter(YearGroup.year == year_num).all()
        year_group_ids = [yg.yeargroup_id for yg in year_groups]
        
        if year_group_ids:
            classes = Class.query.filter(Class.yeargroup_id.in_(year_group_ids)).all()
            class_ids = [c.class_id for c in classes]
            
            if class_ids:
                query_filters.append(Student.class_id.in_(class_ids))
    
    if query_filters:
        students = Student.query.filter(and_(*query_filters)).limit(50).all()
        
        for student in students:
            class_info = Class. query.get(student .class_id)
            year_group_obj= YearGroup .query.get (class_info. yeargroup_id )if class_info else None
            
            grades_data = get_student_grades(student.student_id)
            
            results.append({
                'student_id':student. student_id,
                'name': f"{student .first_name} {student.last_name}",
                'first_name': student. first_name,
                'last_name': student. last_name,
                'class': class_info .class_code if class_info else 'Unknown',
                'year_group': year_group_obj .year if year_group_obj else 'Unknown',
                'ethnicity': student. ethnicity or 'Not specified',
                'home_language': student .home_language or 'Not specified',
                'reading_age': student. reading_age or 'Not specified',
                'grades': grades_data
            })
    
    return results

def get_student_grades(student_id):
    """Get grades for a specific student across all terms"""
    try:
        terms = Terms .query. order_by(Terms .term_id.desc()). limit(4).all()
        grades_data = {}
        
        for term in terms:
            language_grade = Grades .query. filter_by(
                student_id=student_id, 
                term_id=term .term_id, 
                subject_id=1
            ).first()
            
            literature_grade = Grades.query.filter_by(
                student_id=student_id, 
                term_id=term.term_id, 
                subject_id=2
            ). first()
            
            if language_grade and literature_grade:
                grades_data[term. term_name] = language_grade.grade
            elif language_grade:
                grades_data[term .term_name] = language_grade.grade
            elif literature_grade:
                grades_data[term. term_name] = literature_grade.grade
            else:
                grades_data[term.term_name] = 'N/A'
        
        return grades_data
    except Exception as e:
        print(f"Error getting grades for student {student_id}: {str(e)}")
        return {}
