
# from alchemy_db import db.Model
from sqlalchemy import  MetaData, ForeignKey
from flask_login import login_user, UserMixin
from sqlalchemy.orm import backref, relationship
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from app import app

db = SQLAlchemy()


#from app import login_manager

metadata = MetaData()



#Users class, The class table name 'h1t_users_cvs'
class user(db.Model,UserMixin):

    
    __tablename__ = 'user'
    # __table_args__ = {'extend_existing': True}

    #Create db.Columns
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    image = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(120),unique=True)
    password = db.Column(db.String(120), unique=True)
    token = db.Column(db.String(255), unique=True,nullable=True)
    # staysigned = db.Column(db.Boolean, default=False)
    confirm_password = db.Column(db.String(120), unique=True)
    verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(120))

    __mapper_args__={
        "polymorphic_identity":'user',
        'polymorphic_on':role
    }



class job_user(user):

    __tablename__ = 'job_user'

    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    school = db.Column(db.String(120))
    tertiary = db.Column(db.String(30))
    contacts = db.Column(db.String(20))
    experience = db.Column(db.String(500))
    skills = db.Column(db.String(500))
    hobbies = db.Column(db.String(120))
    address = db.Column(db.String(120))
    reference_1 = db.Column(db.String(120))
    reference_2 = db.Column(db.String(120))
    other = db.Column(db.String(120))
    jobs_applied_for = relationship("Applications", backref='Applications.job_title', lazy=True)

    __mapper_args__={
            "polymorphic_identity":'job_user'
        }


class company_user(user):

    __tablename__ = 'company_user'
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    company_address = db.Column(db.String(120))
    company_contacts = db.Column(db.String(120))
    web_link = db.Column(db.String(120))
    fb_link = db.Column(db.String(120))
    twitter_link = db.Column(db.String(120))
    youtube = db.Column(db.String(120))
    other = db.Column(db.String(120))
    job_ads = relationship("Jobs_Ads", backref='Jobs_Ads.job_title',lazy=True)
    applicantions_posted = relationship("Applications", backref='employer', lazy=True)
    freelance_job_ads = relationship("Freelance_Jobs_Ads", backref='Freelance_Jobs_Ads.service_title', lazy=True)

    __mapper_args__ = {
        "polymorphic_identity": 'company_user'
    }

class Email_Verifications(db.Model, UserMixin):

    __table_name__='email_verifications'

    email_id = db.Column(db.Integer,ForeignKey('user.id'), primary_key=True)
    generated_hash = db.Column(db.String(120))
    time_stamp = db.DateTime()

    # __abstract__ = True

class Jobs_Ads(db.Model, UserMixin):

    __tablename__ = "job_ads"

    job_id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(20))
    pay_type = db.Column(db.String(20))
    job_type = db.Column(db.String(20))
    category = db.Column(db.String(255))
    description = db.Column(db.String(200))
    work_duration = db.Column(db.String(60))
    work_days = db.Column(db.String(60))
    work_hours = db.Column(db.String(60))
    responsibilities = db.Column(db.String(200))
    qualifications = db.Column(db.String(200))
    age_range = db.Column(db.String(60))
    benefits = db.Column(db.String(200))
    application_deadline = db.Column(db.DateTime, nullable=False)
    contact_person = db.Column(db.String(40))
    other = db.Column(db.String(120))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) #Records itself
    job_posted_by = db.Column(db.Integer, ForeignKey('company_user.id'),nullable=False) #Records itself
    applicantions = relationship("Applications", backref='All Applications', lazy=True)



class Applications(db.Model, UserMixin):

    __tablename__ = 'job_applications'

    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, ForeignKey('job_user.id'),nullable=False)
    employer_id = db.Column(db.Integer, ForeignKey('company_user.id'), nullable=False)
    jfreel_job_details_id = db.Column(db.Integer, ForeignKey('job_ads.job_id'), nullable=False)
    other = db.Column(db.String(120))
    time_stamp = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
    closed = db.Column(db.String(200))

class FreeL_Applications(db.Model, UserMixin):

    __tablename__ = 'freelance_applications'

    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, ForeignKey('job_user.id'),nullable=False)
    employer_id = db.Column(db.Integer, ForeignKey('company_user.id'), nullable=False)
    other = db.Column(db.String(120))
    freel_job_details_id = db.Column(db.Integer, ForeignKey('freelance_job_ads.job_id'), nullable=False)
    time_stamp = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
    closed = db.Column(db.String(200))


class Freelance_Jobs_Ads(db.Model, UserMixin):

    __tablename__ = "freelance_job_ads"

    job_id = db.Column(db.Integer, primary_key=True)
    service_title = db.Column(db.String(20))  #e.g Logo Design
    service_category = db.Column(db.String(20))   #e.g Design & Technology
    specialty = db.Column(db.String(20))      #e.g Graphic Designer
    description = db.Column(db.String(200))
    project_duration = db.Column(db.String(60))  #Project duration
    other = db.Column(db.String(200))
    application_deadline = db.Column(db.DateTime, nullable=False)
    contact_person = db.Column(db.String(40))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    job_posted_by = db.Column(db.Integer, ForeignKey('company_user.id'),nullable=False) #Records itself
    applications = relationship("FreeL_Applications", backref='FreeL_Applications.id', lazy=True)

class testimonials(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    title = db.Column(db.String(10)) #db.Column(db.Boolean, default=False)
    occupation = db.Column(db.String(80))
    company = db.Column(db.String(80))
    testimony = db.Column(db.String(200))
    image = db.Column(db.String(120))