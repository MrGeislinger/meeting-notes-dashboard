from flask import render_template
from dashboardapp import app, db
from database import actions
from database.models import Cohort, Student

from datetime import datetime, timedelta

@app.route('/')
@app.route('/index')
def index():
    # TODO: Default page
    return render_template('index.html')

@app.route('/create-db')
def create_db():
    '''
    Creates database.
    '''
    print('Create database...')
    actions.create_db()
    return render_template(
                'base-template.html',
                data = ['Database created']
    )

@app.route('/all-cohorts')
@app.route('/cohorts')
def display_all_cohorts():
    '''
    Displays all cohorts already created.
    '''
    print('Looking up Cohorts in database...')
    # TODO: Create more filters for cohorts (graduated, pacing, etc.)
    all_cohorts = Cohort.query.all()
    return render_template(
                'cohorts.html',
                all_cohorts = all_cohorts
    )


@app.route('/create-cohort')
def create_cohort():
    '''
    Creates entry in database of a new cohort.
    '''
    print('Creating Cohort...')
    # TODO: Ask for data to create cohort
    actions.create_cohort('New Cohort',datetime.now())
    return render_template('index.html')

@app.route('/one-on-one')
@app.route('/1-on-1')
@app.route('/1-1')
def project_one():
    '''
    Page for when on a one-on-one call. Allows for input notes to the database
    for the call.
    '''
    # TODO: Find relevant meeting (student) by time for apppointment
    # TODO: Get current event name to display
    # event_name = event['summary']
    event_name = 'NAME OF EVENT'

    # Date display format
    DATE_FORMAT_STRING = '%H:%M - %a %b %d'
    # TODO: Get time of event (start and end)
    now = datetime.now()
    event_time_start = now.strftime(DATE_FORMAT_STRING)
    event_time_end = (now + timedelta(0,30*60)).strftime(DATE_FORMAT_STRING)

    # TODO: Pull other information relevant for template (from event)
    student_name = 'STUDENT NAME'
    zoom_link = 'https://example.com/zoomlink'

    # TODO: Pull info from database
    prev_status = 'Previous status for student updates'

    return render_template(
        'one-on-one.html',
        student_name = student_name,
        zoom_link = zoom_link,
        status = prev_status,
        event_name = event_name,
        event_time_start = event_time_start,
        event_time_end = event_time_end
    )
