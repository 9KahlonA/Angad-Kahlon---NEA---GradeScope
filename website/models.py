from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model): # Defines the user to model from data pulled from the database
    __tablename__ = 'users'  # Defiones the table name
    id = db.Column('user_id', db.Integer, primary_key=True)  # Sets the id tag to user_id in the db (Primary Key)
    username = db.Column(db.String(150), unique=True, nullable=False)  # Makes sure username are max 150 characters long and unique
    password_hash = db.Column(db.String(150), nullable=False) # Makes sure the passwordm which is hashed, is max 150 characters long and not null

    def set_password(self, password): # 
        self.password_hash = generate_password_hash(password) # Hashes the Password using PBKDF2 and the SHA256 algorithm provided in the werkzeug.security module

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) # Checks the password against the hashed passwords in the db

class YearGroup(db.Model):
    __tablename__ = 'yeargroups'  # Correct table name
    yeargroup_id = db.Column(db.Integer, primary_key=True)  # Correct primary key
    year = db.Column(db.String(50), nullable=False)

class Class(db.Model):
    __tablename__ = 'classes'  # Correct table name
    class_id = db.Column(db.Integer, primary_key=True)  # Correct primary key
    class_code = db.Column(db.String(50), nullable=False)
    yeargroup_id = db.Column(db.Integer, db.ForeignKey('yeargroups.yeargroup_id'), nullable=False)  # Correct foreign key

class Subject(db.Model):
    __tablename__ = 'subjects'  # Correct table name
    subject_id = db.Column(db.Integer, primary_key=True)  # Correct primary key
    subject_name = db.Column(db.String(100), nullable=False)  # Correct column name

class Terms(db.Model):
    __tablename__ = 'terms'  # Correct table name
    term_id = db.Column(db.Integer, primary_key=True)  # Correct primary key
    term_name = db.Column(db.String(100), nullable=False)  # Correct column name

class Grades(db.Model):
    __tablename__ = 'grades'  # Correct table name
    grade_id = db.Column(db.Integer, primary_key=True)  # Correct primary key
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)  # Correct foreign key
    term_id = db.Column(db.Integer, db.ForeignKey('terms.term_id'), nullable=False)  # Corrected foreign key
    grade = db.Column(db.String(10), nullable=False)

class Student(db.Model):
    __tablename__ = 'students'  # Correct table name
    student_id = db.Column(db.Integer, primary_key=True)  # Correct primary key
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    ethnicity = db.Column(db.String(50), nullable=True)
    home_language = db.Column(db.String(50), nullable=True)
    reading_age = db.Column(db.Float, nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False)  # Correct foreign key