from website.templates import create_app  # Adjust the import path to match the module structure
app = create_app()

if __name__ == '__main__':  # Run the app in debug mode for development without having to reload every time.
    app.run(debug=False)  # Ensure debug mode is off in production