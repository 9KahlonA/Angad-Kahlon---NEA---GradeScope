from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:GradescopeDev@localhost/gradescope_db'  # Update with your MySQL credentials
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Remove or comment out db.create_all() if the database schema already exists
    # with app.app_context():
    #     db.create_all()

    # Register blueprints
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    return app
