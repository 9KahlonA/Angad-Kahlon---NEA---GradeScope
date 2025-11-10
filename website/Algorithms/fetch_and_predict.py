from ..models import Student, Class, Grades, Terms, Subject
from ..Algorithms.Prediction_Model import Student as PredictStudent, GradePredictor
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Fetches student data from the GradeScope database
# converts data into a format that can be used by the prediction model
def fetch_student_for_prediction(student_id, db):
    student_obj = Student.query.get(student_id)
    if not student_obj:
        return None, None

    class_obj = Class.query.get(student_obj.class_id)
    year_group = int(class_obj.yeargroup_id) + 6

    # Creates a student object, with matching atrtributes for the model.
    pred_student = PredictStudent(
        student_id=student_obj.student_id,
        reading_age=student_obj.reading_age or 11.0,
        is_efl=1 if student_obj.home_language.lower() != "english" else 0,
        ethnicity=student_obj.ethnicity or "Unknown",
        current_year=year_group,
        first_name=student_obj.first_name,
        last_name=student_obj.last_name,
        class_code=class_obj.class_code
    )

    # Retrieves the correct grades for the student across all subjects and terms
    subjects = Subject.query.all()
    terms = Terms.query.order_by(Terms.term_id).all()

    for subj in subjects:
        grades = {}
        for term in terms:
            g = Grades.query.filter_by(student_id=student_id, subject_id=subj.subject_id, term_id=term.term_id).first()
            if g and str(g.grade).isdigit():
                grades[term.term_name] = float(g.grade)
        if grades:
            pred_student.add_grades(subj.subject_name, grades)

    return pred_student, class_obj.class_code

#' Creates a plot from the prediction models data and saves it in the assets folder
def generate_plot(data):
    plt.plot(data)
    plt.savefig('static/assets/graph.png')
    plt.close()
