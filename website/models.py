from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'  # Correct table name
    id = db.Column('user_id', db.Integer, primary_key=True)  # Map 'id' to 'user_id'
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class YearGroup(db.Model):
    __tablename__ = 'yeargroups'  # Correct table name
    __table_args__ = {'schema': 'gradescope'}  # Specify the schema
    yeargroup_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(50), nullable=False)

class Class(db.Model):
    __tablename__ = 'classes'
    class_id = db.Column(db.Integer, primary_key=True)  # Correct column name
    class_code = db.Column(db.String(50), nullable=False)  # Correct column name
    yeargroup_id = db.Column(db.Integer, db.ForeignKey('gradescope.yeargroups.yeargroup_id'), nullable=False)  # Correct column name

class Subject(db.Model):
    __tablename__ = 'subjects'  # Correct table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Terms(db.Model):
    __tablename__ = 'terms'
    term_id = db.Column(db.Integer, primary_key=True)
    term_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Terms(term_id={self.term_id}, term_name='{self.term_name}')>"

class Grades(db.Model):
    __tablename__ = 'grades'
    __table_args__ = {'extend_existing': True}  # Allow redefinition if the table already exists

    grade_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    subject_id = db.Column(db.Integer, nullable=False)  # Assuming subject IDs are predefined
    term_id = db.Column(db.Integer, db.ForeignKey('terms.term_id'), nullable=False)
    grade = db.Column(db.String(10), nullable=False)  # Grade as a string (e.g., "A", "B", etc.)

    def __repr__(self):
        return f"<Grades(grade_id={self.grade_id}, student_id={self.student_id}, subject_id={self.subject_id}, term_id={self.term_id}, grade='{self.grade}')>"

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)  # Ensure this matches the database column
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    ethnicity = db.Column(db.String(50), nullable=True)  # Ensure this field exists
    home_language = db.Column(db.String(50), nullable=True)  # Ensure this field exists
    reading_age = db.Column(db.Float, nullable=True)  # Ensure this field exists
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False)