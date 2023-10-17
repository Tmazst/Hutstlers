from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, TextAreaField,BooleanField
from wtforms.validators import DataRequired,Length,Email, EqualTo, ValidationError
from flask_login import current_user
from flask_wtf.file import FileField , FileAllowed



class Register(FlaskForm):

    name = StringField('name', validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm = PasswordField('confirm', validators=[DataRequired(),EqualTo('password'), Length(min=8, max=64)])

    submit = SubmitField('Create Account!')


    def validate_email(self,email):
        from app import db, user

        user_email = user.query.filter_by(email = self.email.data).first()
        if user_email:
            raise ValidationError(f"email, {email.value}, already taken by someone")



class Login(FlaskForm):


    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=64)])
    submit = SubmitField('Login')


class Contact_Form(FlaskForm):

    name = StringField('name')
    email = StringField('email', validators=[DataRequired(),Email()])
    subject = StringField("subject")
    message = TextAreaField("Message",validators=[Length(min=8, max=2000)])
    submit = SubmitField("Send")


def open_passchange_gui():
    return True

class Update_account_form(FlaskForm):


    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image_pfl = FileField('Profile Image', validators=[FileAllowed(['jpg','png'])])
    contacts = StringField('Contact(s)', validators=[Length(min=8, max=64)])
    school = StringField('High School', validators=[Length(min=8, max=64)])
    tertiary = StringField('Tertiary (Optional)')
    experience = TextAreaField('Work Experience (Optional)')
    skills = TextAreaField('Skills', validators=[Length(min=8, max=150)])
    hobbies = StringField('Hobbies (Optional)')
    address = StringField('Physical Address', validators=[DataRequired(), Length(min=8, max=100)])
    reference_1 = TextAreaField('Reference 1 [Fullname & Contact]',
                                validators=[DataRequired(), Length(min=8, max=64)])
    reference_2 = TextAreaField('Reference 2  [Fullname & Contact]',
                                validators=[DataRequired(), Length(min=8, max=64)])

    def validate_email(self,email):
        from app import db, user
        if current_user.email != self.email.data:
            #Check if email exeists in database
            user_email = user.query.filter_by(email = self.email.data).first()
            if user_email:
                raise ValidationError(f"email, {email.value}, already taken by someone")


    update = SubmitField('Update')


class Reset(FlaskForm):

    old_password = PasswordField('old password', validators=[DataRequired(), Length(min=8, max=64)])
    new_password = PasswordField('new password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('new_password'), Length(min=8, max=64)])

    reset = SubmitField('Reset')


class Reset_Request(FlaskForm):

    email = StringField('email', validators=[DataRequired(), Email()])

    reset = SubmitField('Submit')

    # def validate_email(self,email):
    #     user = user.query.filter_by