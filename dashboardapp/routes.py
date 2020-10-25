# Flask app
from flask import render_template, request
from dashboardapp import app, db
# Database
from database import actions
from database.models import Cohort, Student
# Getting events (Google API)
from events import google_events as gcal
# Other necessary libraries
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


@app.route('/create-cohort', methods=['GET','POST'])
def create_cohort():
    '''
    Creates entry in database of a new cohort.
    '''
    print('Creating Cohort...')
    # Ask for data to create cohort
    cohort_name = request.form.get('cohort_name')
    cohort_start = request.form.get('cohort_start')
    cohort_grad = request.form.get('cohort_grad')
    # Check if required entries are included 
    if cohort_name and cohort_start:
        # Convert strings into datetime
        cohort_start = datetime.strptime(
            cohort_start,
            '%Y-%m-%d'
        )
        # Only attempt if graduation date given
        if cohort_grad:
            cohort_grad = datetime.strptime(
               cohort_grad,
               '%Y-%m-%d'
            )
        else:
            cohort_grad = None
        actions.create_cohort(cohort_name,cohort_start,cohort_grad)
    # Use method to display all cohorts
    return display_all_cohorts()

@app.route('/one-on-one')
@app.route('/1-on-1')
@app.route('/1-1')
def project_one():
    '''
    Page for when on a one-on-one call. Allows for input notes to the database
    for the call.
    '''

    # Date display format
    DATE_FORMAT_STRING = '%H:%M - %a %b %d'
    # Get time of event (start and end)
    now = datetime.now()
    events = gcal.get_one_on_one_events(now)
    event = gcal.get_current_one_on_one(events)

    # Change format (using datetime)
    DATE_FORMAT_IN = '%Y-%m-%dT%H:%M:%S-'
    event_time_start = datetime.strptime(
                            event.get('start').get('dateTime')[:-5],
                            DATE_FORMAT_IN
    )
    event_time_end = datetime.strptime(
                            event.get('end').get('dateTime')[:-5],
                            DATE_FORMAT_IN
    )
    event_time_start = datetime.strftime(event_time_start,DATE_FORMAT_STRING)
    event_time_end = datetime.strftime(event_time_end,DATE_FORMAT_STRING)

    # Pull other information relevant for template (from event)
    # TODO: Some sort of name override (for misspellings or different spellings)
    event_name = event.get('summary')
    # TODO: Ensure this is a URL
    zoom_link = event.get('location')

    # TODO: Pull info from database
    prev_status = 'Previous status for student updates'

    return render_template(
        'one-on-one.html',
        event_name = event_name,
        zoom_link = zoom_link,
        status = prev_status,
        event_time_start = event_time_start,
        event_time_end = event_time_end,
        extra_debug = ''
    )
