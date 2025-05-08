from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model): # Defines the user to model from data pulled from the database
    __tablename__ = 'users'  # Defiones the table name
    id = db.Column('user_id', db.Integer, primary_key=True)  # Sets the id tag to user_id in the db (Primary Key)
    username = db.Column(db.String(150), unique=True, nullable=False)  # Makes sure username are max 150 characters long and unique
    password_hash = db.Column(db.String(150), nullable=False) # Makes sure the passwordm which is hashed, is max 150 characters long and not null

    def set_password(self, password): # 
        self.password_hash = generate_password_hash(password) # Hashes the Password using the MD5 algorithm provided in the werkzeug.security module

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) # Checks the password against the hashed passwords in the db

class YearGroup(db.Model):
    __tablename__ = 'yeargroups'  # Defines the table name 
    __table_args__ = {'schema': 'gradescope'}  # Specify the schema
    yeargroup_id = db.Column(db.Integer, primary_key=True) # sets the yeargroup_id as the primary key
    year = db.Column(db.String(50), nullable=False) # Year is set to a string, max 50 characters long and not null

class Class(db.Model):
    __tablename__ = 'classes' # Defines the table name
    class_id = db.Column(db.Integer, primary_key=True)  #sets the class_id as the primary key
    class_code = db.Column(db.String(50), nullable=False)  # sets the class_code to a string, max 50 characters long and not null
    yeargroup_id = db.Column(db.Integer, db.ForeignKey('gradescope.yeargroups.yeargroup_id'), nullable=False)  # foreign key to link to yeargroups table

class Subject(db.Model):
    __tablename__ = 'subjects'  # Defines the table name
    id = db.Column(db.Integer, primary_key=True) # sets the id as the primary key and integer
    name = db.Column(db.String(100), nullable=False) # sets the name to a string, max 100 characters long and not null

class Terms(db.Model):
    __tablename__ = 'terms' # Defines the table name
    term_id = db.Column(db.Integer, primary_key=True) # sets the term_id as the primary key and integer
    term_name = db.Column(db.String(100), nullable=False) # sets the term_name to a string, max 100 characters long and not null

    def __repr__(self):
        return f"<Terms(term_id={self.term_id}, term_name='{self.term_name}')>"

class Grades(db.Model):
    __tablename__ = 'grades' # Defines the table name
    __table_args__ = {'extend_existing': True}  # allows for the table to be extended if it already exists

    grade_id = db.Column(db.Integer, primary_key=True) # sets the grade_id as the primary key and integer
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False) # Foreign key to link to student table
    subject_id = db.Column(db.Integer, nullable=False)  # Foreign key to link to subject table     
    term_id = db.Column(db.Integer, db.ForeignKey('terms.term_id'), nullable=False) # Foreign key to link to terms table
    grade = db.Column(db.String(10), nullable=False)  # sets the grade to a string, max 10 characters long and not null

    def __repr__(self):
        return f"<Grades(grade_id={self.grade_id}, student_id={self.student_id}, subject_id={self.subject_id}, term_id={self.term_id}, grade='{self.grade}')>"
    # Provides a string representation of the grades table to use in debugginng as i ran inot some errors.

class Student(db.Model):
    __tablename__ = 'students' # Defines the table name
    student_id = db.Column(db.Integer, primary_key=True)  # sets the student_id as the primary key and integer
    first_name = db.Column(db.String(50), nullable=False) # sets the first_name to a string, max 50 characters long and not null
    last_name = db.Column(db.String(50), nullable=False) # sets the last_name to a string, max 50 characters long and not null
    ethnicity = db.Column(db.String(50), nullable=True)  # sets the ethnicity to a string, max 50 characters long and not null
    home_language = db.Column(db.String(50), nullable=True)  # sets the home_language to a string, max 50 characters long and not null
    reading_age = db.Column(db.Float, nullable=True)  # sets the reading_age to a float, max 50 characters long and not null
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False) # Foreign key to link to classes table