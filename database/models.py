from dashboardapp import db

class Student(db.Model):
    '''
    Details about student. Note 
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    # cohort
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.id'),
        nullable=False)
    cohort = db.relationship('Cohort',
        backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Student {self.name}>'


class Cohort(db.Model):
    '''
    Cohort of students. Students can transfer in and out of cohorts at any given
    time.
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    graduation_date = db.Column(db.DateTime, nullable=True, default=None)

    def __repr__(self):
        return f'<Cohort {self.name}>'

class Meeting(db.Model):
    '''
    Some type of meeting 
    '''
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    # TODO: Include participants
    event_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<{self.event_type} Meeting on {self.date}>'

class Note(db.Model):
    '''
    '''
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(180), unique=False, nullable=True)
    details = db.Column(db.String(800), unique=False, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    # New note, new meeting
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'),
        nullable=False)
    meeting = db.relationship('Meeting',
        backref=db.backref('posts', lazy=True))
    # Associated with the student
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
        nullable=False)
    student = db.relationship('Student',
        backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Note "{self.status}">'
