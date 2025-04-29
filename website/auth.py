from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    print(f"Request method: {request.method}")  # Debug statement
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Username: {username}, Password: {password}")  # Debug statement

        user = User.query.filter_by(username=username).first()
        if user:
            print(f"User found: {user.username}")  # Debug statement
            print(f"Stored password hash: {user.password_hash}")  # Debug statement
        else:
            print("User not found")  # Debug statement

        if user and user.check_password(password):
            print("Password verification successful")  # Debug statement
            flash('Login successful!', category='success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Incorrect username or password', category='error')
            print("Password verification failed")  # Debug statement
    return render_template('login.html')

@auth.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')