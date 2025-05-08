from website import create_app # Import the create_app function from the website package

app = create_app() # Create an instance of the Flask application using the create_app function

if __name__ == '__main__': # Check if this script is being run directly (not imported as a module)
    app.run(debug=True) # Run the Flask application in debug mode, which provides detailed error messages and auto-reloads the server on code changes
'# When this script is run, it will start the Flask application and make it accessible at http://127.0.0.1:5000/login'