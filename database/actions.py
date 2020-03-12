from dashboardapp import db
from database.models import Cohort, Student



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
