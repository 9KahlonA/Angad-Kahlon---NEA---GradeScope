# Import database models
from ..models import Student, Class, Grades, Terms, Subject

# Import the predictive model structure
from ..Algorithms.Predition_Model import Student as PredictStudent, GradePredictor

import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-GUI environments

import matplotlib.pyplot as plt

# Fetch a student's academic profile from the DB and convert it into a prediction-ready object
def fetch_student_for_prediction(student_id, db):
    student_obj = Student.query.get(student_id)  # Get the student record by ID
    if not student_obj:
        return None, None  # Return None if not found

    class_obj = Class.query.get(student_obj.class_id)  # Get class info to extract year group
    year_group = int(class_obj.yeargroup_id) + 6  # Convert yeargroup_id (e.g. 1) ➜ school year (e.g. Year 7)

    # Create PredictStudent object with features used for ML projection
    pred_student = PredictStudent(
        student_id=student_obj.student_id,
        reading_age=student_obj.reading_age or 11.0,  # Default reading age if null
        is_efl=1 if student_obj.home_language.lower() != "english" else 0,  # Mark as EFL if not English
        ethnicity=student_obj.ethnicity or "Unknown",
        current_year=year_group
    )

    subjects = Subject.query.all()  # Fetch all available subjects
    terms = Terms.query.order_by(Terms.term_id).all()  # Ordered terms to map progression

    # Loop through subjects to pull their grades for the student
    for subj in subjects:
        grades = {}
        for term in terms:
            g = Grades.query.filter_by(student_id=student_id, subject_id=subj.subject_id, term_id=term.term_id).first()  # Corrected subject_id
            if g and str(g.grade).isdigit():  # Only process numeric grades
                grades[f"Year {year_group}"] = float(g.grade)
        if grades:
            pred_student.add_grades(subj.subject_name, grades)  # Corrected subject_name

    return pred_student, class_obj.class_code  # Return the structured student + class info

def generate_plot(data):
    plt.plot(data)
    plt.savefig('static/assets/graph.png')  # Save the plot to a file
    plt.close()  # Close the plot to release resources
