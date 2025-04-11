from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'GradesScopeDEV' # Change this to a random secret key in production


    from .views import views
    from .auth import auth

    app.register_blueprint(views, name="VIEWS", url_prefix='/')
    app.register_blueprint(auth, name="AUTH", url_prefix='/')

    return app

# This file is reponsible for creating the instance for the Flask app. DO NOT MODIFY THIS FILE.
