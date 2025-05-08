from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
#Imports the User model created in models.py and imports thes necessary flash modules

auth = Blueprint('auth', __name__) # Creates the auth blueprint to be used throughout the Flask app

# GET is used to retrieve data from the database
# POST is used to send data to the database
@auth.route('/login', methods=['GET', 'POST']) # Creates the login route for the auth blueprint 
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Check if the username and password match a user in the users table

        user = User.query.filter_by(username=username).first() # Checks against the database
        if user and user.check_password(password): # Checks the password against the macthed user record
            flash('Login successful!', category='success') # Success Message
            return redirect(url_for('auth.dashboard')) # Redirects to the dashboard page through its route
        else:
            flash('Incorrect username or password', category='error') # Error Message
    return render_template('login.html') # Returns to the login page

@auth.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
# Defines the dashboard route from the auth blueprint
# Could not get this route to work outside of the auth blueprint, so it is in here for no