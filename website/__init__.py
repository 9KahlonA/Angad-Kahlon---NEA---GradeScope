from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# This is required for PyMySQL to work with MySQL's sha256_password or caching_sha2_password hashing methods
import pymysql

db = SQLAlchemy()

def create_app() : #creates the app locally in a function rather than globally
    app =Flask(__name__)
    app.config[ 'SECRET_KEY'] ='GradeScope'
    app.config['SQLALCHEMY_DATABASE_URI' ]= 'mysql+pymysql://root:GradescopeDev@localhost/gradescope?charset=utf8mb4'
    app.config ['SQLALCHEMY_TRACK_MODIFICATIONS']  = False #Monitors changes
    app.config[ 'WTF_CSRF_ENABLED']= False #prevents crsf attacks

    db. init_app(app)

    from .auth import auth #allows the code to be written in chcunks rather than all in one file
    from . views import views
    app .register_blueprint( auth, url_prefix='/')
    app. register_blueprint(views , url_prefix='/')

    return app


