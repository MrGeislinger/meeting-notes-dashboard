from dashboardapp import db
from database.models import Cohort, Student, Meeting, Note



def create_db():
    '''
    '''
    db.create_all()
    print('Database created')

def create_cohort(cohort_name, start_date, graduation_date=None):
    '''
    '''
    new_cohort = Cohort(
                    name=cohort_name,
                    start_date=start_date,
                    graduation_date=graduation_date
    )
    db.session.add(new_cohort)
    db.session.commit()
    print('Cohort created')

def add_student(name, email, cohort):
    '''
    '''
    new_student = Student(
        name=name,
        email=email,
        cohort_id=cohort
    )
    db.session.add(new_student)
    db.session.commit()
    print('Student added')

def new_meeting(meeting_time, event_type):
    '''
    '''
    new_meeting = Meeting(
        date=meeting_time,
        event_type=event_type
    )
    db.session.add(new_meeting)
    db.session.commit()
    print('Meeting created')
    # Return the entry created for reference
    return new_meeting

def add_note(note, meeting_id, student_id, status=None):
    '''
    '''
    new_note = Note(
        details=note,
        status=status,
        meeting_id=meeting_id,
        student_id=student_id
    )
    db.session.add(new_note)
    db.session.commit()
    print('Note added')