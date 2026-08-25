**GradeScope
**
GradeScope is a full-stack web application developed as my A Level Computer Science NEA. The system is designed to help students understand their academic progress by providing grade information and predicting potential future grades.

Overview

The project combines a web application, relational database and prediction algorithm into a single system.

GradeScope allows users to:

- View student and grade information
- Organise students by year group and class
- Record grades across different subjects and terms
- Generate predicted grades
- View projected academic performance through visualisations

The prediction system uses a range of factors to produce realistic grade predictions, with the aim of providing a more personalised projection of student performance.

Technologies

Backend

- Python
- Flask
- SQLAlchemy
- PyMySQL

Frontend

- HTML
- CSS
- JavaScript

Database

- MySQL

Data & Visualisation

- NumPy
- Matplotlib

Prediction System

The prediction system is built around several components that work together to generate a student's predicted grade.

These include:

- Grade Predictor – Main prediction engine
- Modifier Engine – Applies relevant student factors to predictions
- Growth Calculator – Calculates expected academic growth
- Grade Limiter – Ensures predictions remain appropriate for the student's year group
- Challenge Simulator – Introduces realistic variation into predictions

Predictions are generated using a student's existing information and are seeded using their student ID to ensure consistent results.

Database

GradeScope uses a relational MySQL database to store and manage application data.

The database includes relationships between:

"Year Groups → Classes → Students → Grades"

alongside subjects and academic terms.

SQLAlchemy is used as the ORM to interact with the database from the Flask application.

Security

Security and data protection were considered throughout development.

The application includes server-side validation and input sanitisation, including protection against potentially malicious search input. The application was also designed to run within a school's local network rather than being publicly accessible.

Development

This project was developed from the ground up as part of my A Level Computer Science NEA, covering the full software development process from planning and database design through to implementation, testing and evaluation.

The project gave me practical experience with full-stack development, databases, algorithms, data analysis and software security.

Project Structure

GradeScope/
├── website/
│   ├── auth.py
│   ├── views.py
│   ├── models.py
│   ├── templates/
│   └── static/
├── main.py
├── requirements.txt
└── README.md

Author

Angad Kahlon

Computer Science student at the University of Surrey.

"GitHub" (https://github.com/9kahlona)
