from flask import Flask, render_template

app = Flask(__name__)

@app.route('/auth.login')
def login():
    return render_template('login.html')

@app.route('/graph')
def graph_page():
    return render_template('student_projections.html')

if __name__ == '__main__':
    app.run(debug=True)