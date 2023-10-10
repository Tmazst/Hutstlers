
from alchemy_db import Base
from sqlalchemy import Integer, String, Column, MetaData, Boolean, ForeignKey, DateTime
from flask_login import login_user, UserMixin
from sqlalchemy.orm import backref, relationship
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer



#from app import login_manager

metadata = MetaData()



#Users class, The class table name 'h1t_users_cvs'
class user(Base,UserMixin):

    
    __tablename__ = 'user'
    # __table_args__ = {'extend_existing': True}

    #Create Columns
    id = Column(Integer,primary_key=True)
    name = Column(String(20))
    image = Column(String(30), nullable=True)
    email = Column(String(120),unique=True)
    password = Column(String(120), unique=True)
    confirm_password = Column(String(120), unique=True)
    role = Column(String(120))


    def get_reset_token(self,c_user_id, expires=1800):
        global app
        import app
        s = Serializer(app.app.config['SECRET_KEY'],"confirmation")

        return s.dumps({'user_id':c_user_id})

    @staticmethod
    def verify_reset_token(token):
        import app
        s = Serializer(app.app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return app.db.query(user).get(user_id)

    __mapper_args__={
        "polymorphic_identity":'user',
        'polymorphic_on':role
    }



class job_user(user):

    __tablename__ = 'job_user'

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    school = Column(String(120))
    tertiary = Column(String(30))
    contacts = Column(String(20))
    experience = Column(String(500))
    skills = Column(String(500))
    hobbies = Column(String(120))
    address = Column(String(120))
    reference_1 = Column(String(120))
    reference_2 = Column(String(120))
    jobs_applied_for = relationship("Applications", backref='Applications.job_title', lazy=True)

    __mapper_args__={

            "polymorphic_identity":'job_user'
        }


class company_user(user):

    __tablename__ = 'company_user'
    # __table_args__ = {'extend_existing': True}

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    company_address = Column(String(120))
    company_contacts = Column(String(120))
    web_link = Column(String(120))
    fb_link = Column(String(120))
    twitter_link = Column(String(120))
    youtube = Column(String(120))
    job_ads = relationship("Jobs_Ads", backref='Jobs_Ads.job_title',lazy=True)
    applicantions_posted = relationship("Applications", backref='employer', lazy=True)

    __mapper_args__ = {
        "polymorphic_identity": 'company_user'
    }

class Jobs_Ads(Base, UserMixin):

    __tablename__ = "job_ads"

    job_id = Column(Integer, primary_key=True)
    job_title = Column(String(20))
    pay_type = Column(String(20))
    job_type = Column(String(20))
    description = Column(String(200))
    work_duration = Column(String(60))
    work_days = Column(String(60))
    work_hours = Column(String(60))
    responsibilities = Column(String(200))
    qualifications = Column(String(200))
    age_range = Column(String(60))
    benefits = Column(String(200))
    application_deadline = Column(DateTime, nullable=False)
    contact_person = Column(String(40))
    date_posted = Column(DateTime, default=datetime.utcnow, nullable=False) #Records itself
    print("DEBGU: ",company_user.id)
    job_posted_by = Column(Integer, ForeignKey('company_user.id'),nullable=False) #Records itself
    applicantions = relationship("Applications", backref='All Applications', lazy=True)



class Applications(Base, UserMixin):

    __tablename__ = 'job_applications'

    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey('job_user.id'),nullable=False)
    employer_id = Column(Integer, ForeignKey('company_user.id'), nullable=False)
    job_details_id = Column(Integer, ForeignKey('job_ads.job_id'), nullable=False)
    time_stamp =  Column(DateTime,default=datetime.utcnow, nullable=False)
    closed = Column(String(200))


class Jobs_Ads(Base, UserMixin):

    __tablename__ = "freelance_job_ads"

    job_id = Column(Integer, primary_key=True)
    service_title = Column(String(20))  #e.g Logo Design
    service_category = Column(String(20))   #e.g Design & Technology
    specialty = Column(String(20))      #e.g Graphic Designer
    description = Column(String(200))
    project_duration = Column(String(60))  #Project duration
    work_days = Column(String(60))
    work_hours = Column(String(60))
    responsibilities = Column(String(200))
    qualifications = Column(String(200))
    age_range = Column(String(60))
    benefits = Column(String(200))
    application_deadline = Column(DateTime, nullable=False)
    contact_person = Column(String(40))
    date_posted = Column(DateTime, default=datetime.utcnow, nullable=False) #Records itself
    print("DEBGU: ",company_user.id)
    job_posted_by = Column(Integer, ForeignKey('company_user.id'),nullable=False) #Records itself
    applicantions = relationship("Applications", backref='All Applications', lazy=True)