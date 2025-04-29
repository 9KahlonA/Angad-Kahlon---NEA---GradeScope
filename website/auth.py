from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db

auth = Blueprint('auth', __name__)  # Ensure the name is 'auth'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    print(f"Request method: {request.method}")  # Debug statement to log the request method
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # Redirect to the dashboard page
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Incorrect username or password', category='error')
    return render_template('login.html')

@auth.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')