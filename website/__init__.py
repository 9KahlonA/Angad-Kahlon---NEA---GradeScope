from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Ensure this is set
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:GradescopeDev@localhost/gradescope'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    from .auth import auth
    from .views import views  # Import the views blueprint
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')  # Register the views blueprint

    return app
