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
    # Student met with

    def __repr__(self):
        return f'<{self.event_type} Meeting on {self.date}>'