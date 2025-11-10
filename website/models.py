from . import db
from werkzeug. security import generate_password_hash, check_password_hash

# Database model for user authentication
class User(db . Model):
    __tablename__ = 'users'
    id = db . Column('user_id', db. Integer, primary_key=True)
    username = db . Column(db. String(150), unique=True, nullable=False)
    password_hash = db. Column(db. String(150), nullable=False)

    # Hashes and stores password securely
    def set_password(self, password):
        self . password_hash = generate_password_hash(password)

    # Verifies password against stored hash
    def check_password(self, password):
        return check_password_hash(self. password_hash, password)

# Database model for year groups (Year 7-11)
class YearGroup(db. Model):
    __tablename__ = 'yeargroups'
    yeargroup_id = db . Column(db. Integer, primary_key=True)
    year = db . Column(db. String(50), nullable=False)

# Database model for classes linked to year groups
class Class(db. Model):
    __tablename__ = 'classes'
    class_id = db . Column(db.Integer, primary_key=True)
    class_code = db. Column(db. String(50), nullable=False)
    yeargroup_id = db .Column(db . Integer, db . ForeignKey('yeargroups.yeargroup_id'), nullable=False)

# Database model for subjects (Language, Literature)
class Subject(db . Model):
    __tablename__ = 'subjects'
    subject_id = db.Column(db. Integer, primary_key=True)
    subject_name = db.Column(db . String(100), nullable=False)

# Database model for academic terms
class Terms(db. Model):
    __tablename__ = 'terms'
    term_id = db.Column(db. Integer, primary_key=True)
    term_name = db.Column(db.String(100), nullable=False)

# Database model for student grades linked to student, subject, and term
class Grades(db.Model):
    __tablename__ = 'grades'
    grade_id = db. Column(db. Integer, primary_key=True)
    student_id = db .Column(db .Integer, db .ForeignKey('students. student_id'), nullable=False)
    subject_id = db .Column(db. Integer, db. ForeignKey('subjects. subject_id'), nullable=False)
    term_id = db. Column(db .Integer, db. ForeignKey('terms . term_id'), nullable=False)
    grade = db. Column(db . String(10), nullable=False)

# Database model for student information and attributes
class Student(db. Model):
    __tablename__ = 'students'
    student_id = db. Column(db. Integer, primary_key=True)
    first_name = db .Column(db .String(50), nullable=False)
    last_name = db. Column(db . String(50), nullable=False)
    ethnicity = db .Column(db.String(50), nullable=True)
    home_language = db.Column(db. String(50), nullable=True)
    reading_age = db .Column(db. Float, nullable=True)
    class_id = db . Column(db .Integer, db. ForeignKey('classes.class_id'), nullable=False)