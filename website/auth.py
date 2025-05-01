from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash('Login successful!', category='success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Incorrect username or password', category='error')
    return render_template('login.html')

@auth.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')