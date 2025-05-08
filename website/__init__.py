from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Imports the Flask class from Flask istelf and the SQLAlchemy class form SQLAlchemy which allows us to connect to the database

db = SQLAlchemy() # Initilaises the SQLAlchemyt object

def create_app(): # Defines the function that can create an instance of the Flask App
    app = Flask(__name__) # Creates an instance of the Flask application.
    app.config['SECRET_KEY'] = 'your_secret_key'  # Sets a key that is used to encrypt cookies and other data
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:GradescopeDev@localhost/gradescope'# Specifies what database to connect to
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disables built in tracking of edits to increase peroformanc

    db.init_app(app) # Linkls the db object from SQLAlechemy to the Flask instance

    from .auth import auth # Imports auth blueprint (auth.py)
    from .views import views  # Import views blueprint (views.py)
    app.register_blueprint(auth, url_prefix='/') # Register the auth blueprint to the Flask Instance
    app.register_blueprint(views, url_prefix='/')  # Does the same for views

    return app
