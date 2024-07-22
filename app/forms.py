from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import User, Job, Practice, Doctor
from wtforms import StringField, SelectField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField('Admin Rights')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class JobForm(FlaskForm):
    job_type = SelectField('Type', choices=[
        ('Denture', 'Denture'), 
        ('Bite Plate', 'Bite Plate'), 
        ('Crown', 'Crown'),
        ('Special Tray + Bite', 'Special Tray + Bite'),
        ('Try In', 'Try In'),
        ('Retry', 'Retry'),
        ('Implant Crown', 'Implant Crown'),
        ('Temporary Crown', 'Temporary Crown')
    ])
    practice_name = SelectField('Practice Name', validators=[DataRequired()], coerce=int)
    doctor_name = SelectField('Doctor\'s Name', validators=[DataRequired()], coerce=int)
    patient_name = StringField('Patient\'s Name', validators=[DataRequired()])
    lab_slip_number = StringField('Lab Slip/Order Number', validators=[DataRequired()])
    job_status = SelectField('Job Status', choices=[
        ('In Production', 'In Production'), ('Ready For Delivery', 'Ready For Delivery'), 
        ('In Transit To Practice', 'In Transit To Practice'), 
        ('Delivered by driver', 'Delivered by driver'), ('Delivered by courier', 'Delivered by courier'), ('Hand Over', 'Hand Over')
    ])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    shade = StringField('Shade')
    invoice_number = StringField('Invoice Number')
    delivery_info = StringField('Delivery Information')
    comments = TextAreaField('Comments')  # Add comments field
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.practice_name.choices = [(p.id, p.name) for p in Practice.query.all()]
        self.doctor_name.choices = [(d.id, d.name) for d in Doctor.query.all()]


class PracticeForm(FlaskForm):
    practice_names = TextAreaField('Practice Names (comma separated)', validators=[DataRequired()])
    submit = SubmitField('Add Practices')

class DoctorForm(FlaskForm):
    doctor_names = TextAreaField('Doctor Names (comma separated)', validators=[DataRequired()])
    practice_id = SelectField('Practice', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Add Doctors')

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        self.practice_id.choices = [(p.id, p.name) for p in Practice.query.all()]

class EditJobForm(FlaskForm):
    job_type = SelectField('Job Type', choices=[
        ('Denture', 'Denture'), 
        ('Bite Plate', 'Bite Plate'), 
        ('Crown', 'Crown'), 
        ('Special Tray + Bite', 'Special Tray + Bite'), 
        ('Try In', 'Try In'), 
        ('Retry', 'Retry'), 
        ('Implant Crown', 'Implant Crown'), 
        ('Temporary Crown', 'Temporary Crown')
    ], validators=[DataRequired()])
    practice_name = StringField('Practice Name', validators=[DataRequired()])
    doctor_name = StringField('Doctor Name', validators=[DataRequired()])
    patient_name = StringField('Patient Name', validators=[DataRequired()])
    lab_slip_number = StringField('Lab Slip Number', validators=[DataRequired()])
    job_status = SelectField('Job Status', choices=[
        ('In Production', 'In Production'), ('Ready For Delivery', 'Ready For Delivery'), 
        ('In Transit To Practice', 'In Transit To Practice'), 
        ('Delivered by driver', 'Delivered by driver'), ('Delivered by courier', 'Delivered by courier'), ('Hand Over', 'Hand Over')
    ], validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    shade = StringField('Shade')
    invoice_number = StringField('Invoice Number')
    delivery_info = StringField('Delivery Information')
    comments = TextAreaField('Comments')
    submit = SubmitField('Submit')