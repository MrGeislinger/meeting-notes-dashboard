from dashboardapp import app

from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    # TODO: Default page
    return render_template('index.html')

@app.route('/one-on-one')
@app.route('/1-on-1')
def project_one():
    return render_template('one-on-one.html')
