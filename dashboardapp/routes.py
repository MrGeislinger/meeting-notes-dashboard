# Flask app
from flask import render_template, request
from dashboardapp import app, db
# DatabaseMz
from database import actions
from database.models import Cohort, Student, Meeting, Note
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
    cohort_grad = request.form.get('cohort_graduate')
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

@app.route('/all-students')
@app.route('/students')
def display_all_students():
    return render_template('students.html',all_students=Student.query.all())

@app.route('/add-student', methods=['GET','POST'])
def add_student():
    '''
    '''
    #
    student_name = request.form.get('student_name')
    student_email = request.form.get('student_email')
    student_cohort = request.form.get('student_cohort')
    # Check if entries given (submitted)
    if student_name and student_email and student_cohort:
        print('Adding student')
        actions.add_student(student_name,student_email,student_cohort)
        return render_template('students.html',all_students=Student.query.all())
    # Get all the cohorts to add student to
    all_cohorts = Cohort.query.all()

    return render_template('add-student.html',all_cohorts=all_cohorts)

@app.route('/create-meeting', methods=['GET','POST'])
def create_meeting():
    '''
    '''
    actions.new_meeting(datetime.now(),'1:1')
    return display_all_meetings()

@app.route('/all-meetings')
@app.route('/meetings')
def display_all_meetings():
    '''
    '''
    all_meetings = Meeting.query.all()
    return render_template('base-template.html',data=all_meetings)

@app.route('/one-on-one', methods=['GET','POST'])
@app.route('/1-on-1', methods=['GET','POST'])
@app.route('/1-1', methods=['GET','POST'])
def one_on_one():
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
    
    # TODO: Find Student entry by name
    for test_str in event_name.split('-'):
        test_str = test_str.strip()
        student = Student.query.filter_by(name=test_str).first()
        if student:
            student_id = student.id
            break

    # TODO: Ensure this is a URL
    zoom_link = event.get('location')

    # TODO: Pull info from database
    prev_status = 'Previous status for student updates'

    # On submit
    module = request.form.get('module')
    additional_notes = request.form.get('additional_notes')
    status = request.form.get('status')
    if module:
        now = datetime.now()
        meeting = actions.new_meeting(now,'1:1')
        # 
        actions.add_note(
            note=additional_notes,
            status=status,
            meeting_id=meeting.id,
            student_id=student_id,
            time=now
        )

    # Get past notes
    print('Recent Notes')
    recent_notes = (Note.query.join(Meeting, Meeting.id == Note.meeting_id)
        .filter(Note.student_id==student_id)
        .order_by(Note.time.desc())
        .limit(3).all()
    )
    if recent_notes:
        prev_status = recent_notes[0].status

    return render_template(
        'one-on-one.html',
        event_name = event_name,
        zoom_link = zoom_link,
        status = prev_status,
        event_time_start = event_time_start,
        event_time_end = event_time_end,
        recent_notes=recent_notes,
        extra_debug = ''
    )

@app.route('/all-notes')
@app.route('/notes')
def display_all_notes():
    '''
    '''
    all_notes = Note.query.all()
    return render_template('base-template.html',data=all_notes)
