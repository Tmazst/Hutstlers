from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, TextAreaField,BooleanField
from wtforms.validators import DataRequired,Length,Email, EqualTo, ValidationError,URL
from flask_login import current_user
from wtforms.fields import DateField, TelField
from flask_wtf.file import FileField , FileAllowed

from Forms import Register

class Job_Ads_Form(FlaskForm):


    job_title = StringField('Job Title:', validators=[DataRequired(), Length(min=2, max=20)])
    pay_type_bl = BooleanField('Pay Type:')
    other_pay_type = StringField('Other:')
    other_job_bl = BooleanField('Other Job Type:')
    other_job_type = StringField('Other:')
    description = TextAreaField('Job Description or Tasks:', validators=[DataRequired(), Length(min=5, max=400)])
    work_duration_bl = BooleanField('')
    work_duration = StringField('Work/Project Duration (Start - End):')
    work_days_bl = BooleanField('')
    work_days = StringField('Work Days:')
    work_hours_bl = BooleanField('')
    work_hours = StringField('Work Hours:' )
    responsibilities = TextAreaField('Responsibilities:')
    qualifications = TextAreaField('Requirements or Qualifications:', validators=[DataRequired(), Length(min=5, max=400)])
    age_range_bl = BooleanField('Age Range:')
    age_range = StringField('Age Range:')
    benefits_bl = BooleanField('Benefits:')
    benefits = TextAreaField('Benefits:')
    application_deadline = DateField('Application Deadline:',format="%Y-%m-%d" )
    # application_details = TextAreaField('Application Details', validators=[DataRequired(), Length(min=2, max=20)])
    posted_by = StringField('Posted By:')

    publish = SubmitField("Publish")

class Company_Register_Form(FlaskForm):

    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=20)])
    company_email = StringField('Email', validators=[DataRequired(), Email()])
    company_password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=64)])
    company_confirm = PasswordField('Confirm', validators=[DataRequired(), EqualTo('company_password'), Length(min=8, max=64)])
    company_contacts = TelField('Contact(s)', validators=[Length(min=8, max=64)])
    company_address = StringField('Physical Address', validators=[DataRequired(), Length(min=8, max=100)])
    website_link = StringField('Company Website Link')
    facebook_link = StringField('Facebook Link')
    twitter_link = StringField('Twitter Link')
    youtube_link = StringField('Youtube Link')

    submit = SubmitField('Create Account!')


class Company_UpdateAcc_Form(FlaskForm):

    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=20)])
    company_email = StringField('Email', validators=[DataRequired(), Email()])
    company_logo = FileField('Company Logo', validators=[ FileAllowed(['jpg','png'])])
    company_contacts = StringField('Contact(s)', validators=[Length(min=8, max=64)])
    company_address = StringField('Physical Address', validators=[DataRequired(), Length(min=8, max=100)])
    website_link = StringField('Company Website Link')
    facebook_link = StringField('Facebook Link')
    twitter_link = StringField('Twitter Link')
    youtube_link = StringField('Youtube Link')

    # Validate email before saving it in database
    def validate_email(self,company_email):
        from app import db, company_user
        if current_user.company_email != self.company_email.data:
            #Check if email exeists in database
            cmp_user_email = db.query(company_user).filter_by(company_email = self.company_name.data).first()
            cmp_name = db.query(company_user).filter_by(company_email=self.company_name.data).first()
            if cmp_user_email or cmp_name:
                raise ValidationError(f"email, {company_email.value}, already taken.")

    def validate_company_name(self, company_name):
        from app import db, company_user
        if current_user.comapny_name != self.company_name.data:
            # Check if email exists in database
            cmp_name = db.query(company_user).filter_by(comapny_name=self.company_name.data).first()
            if cmp_name:
                raise ValidationError(f"Company Name, {company_name.value} , already taken.")

    company_submit = SubmitField('Update')

class Company_Login(FlaskForm):


    company_email = StringField('Company email', validators=[DataRequired(),Email()])
    company_password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=64)])
    company_submit = SubmitField('Login')


class Reset(FlaskForm):
    old_password = PasswordField('old password', validators=[DataRequired(), Length(min=8, max=64)])
    new_password = PasswordField('new password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('new_password'), Length(min=8, max=64)])

    reset = SubmitField('Reset')


class Reset_Request(FlaskForm):

    email = StringField('email', validators=[DataRequired(), Email()])

    reset = SubmitField('Submit')