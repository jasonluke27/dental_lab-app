from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, JobForm, PracticeForm, DoctorForm, EditJobForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Job, Practice, Doctor
from werkzeug.urls import url_parse
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
@app.route('/index')
@login_required
def index():
    search_query = request.args.get('search_query', '')
    practice_filter = request.args.get('practice_filter', '')
    doctor_filter = request.args.get('doctor_filter', '')

    jobs_query = Job.query

    if search_query:
        jobs_query = jobs_query.filter(
            Job.patient_name.contains(search_query) |
            Job.lab_slip_number.contains(search_query) |
            Job.invoice_number.contains(search_query)
        )

    if practice_filter:
        jobs_query = jobs_query.filter_by(practice_name=practice_filter)

    if doctor_filter:
        jobs_query = jobs_query.filter_by(doctor_name=doctor_filter)

    jobs = jobs_query.all()
    practices = Practice.query.all()
    doctors = Doctor.query.all()

    return render_template('index.html', title='Home', jobs=jobs, practices=practices, doctors=doctors, search_query=search_query, practice_filter=practice_filter, doctor_filter=doctor_filter)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.is_admin:
        flash('Only administrators can register new users.')
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    if not current_user.is_admin:
        flash('Only administrators can add or edit jobs.')
        return redirect(url_for('index'))
    form = JobForm()
    if form.validate_on_submit():
        job = Job(
            job_type=form.job_type.data,
            practice_name=Practice.query.get(form.practice_name.data).name,
            doctor_name=Doctor.query.get(form.doctor_name.data).name,
            patient_name=form.patient_name.data,
            lab_slip_number=form.lab_slip_number.data,
            job_status=form.job_status.data,
            due_date=form.due_date.data,
            shade=form.shade.data,
            invoice_number=form.invoice_number.data,
            delivery_info=form.delivery_info.data
        )
        logger.debug('Job to be added: %s', job)
        try:
            db.session.add(job)
            db.session.commit()
            flash('Job added successfully!')
        except Exception as e:
            db.session.rollback()
            logger.error('Error adding job: %s', e)
            flash('Error adding job. Please try again.')
        return redirect(url_for('index'))
    return render_template('add_edit_job.html', title='Add Job', form=form)

@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    if not current_user.is_admin:
        flash('Admin access required to edit jobs.')
        return redirect(url_for('index'))
        
    job = Job.query.get_or_404(id)
    form = EditJobForm(obj=job)
    if form.validate_on_submit():
        try:
            print("Raw form data:", request.form)
            job.job_type = form.job_type.data
            job.practice_name = form.practice_name.data
            job.doctor_name = form.doctor_name.data
            job.patient_name = form.patient_name.data
            job.lab_slip_number = form.lab_slip_number.data
            job.job_status = form.job_status.data
            job.due_date = form.due_date.data
            job.shade = form.shade.data
            job.invoice_number = form.invoice_number.data
            job.delivery_info = form.delivery_info.data
            job.comments = form.comments.data

            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            print("Error updating job:", e)
            flash('Error updating job.')
            db.session.rollback()
    else:
        if request.method == 'POST':
            print("Form errors:", form.errors)
            print("Raw form data:", request.form)
            flash('Please correct the errors in the form.')

    return render_template('edit_job.html', title='Edit Job', form=form, job=job)

@app.route('/job/<int:id>')
@login_required
def job(id):
    job = Job.query.get_or_404(id)
    return render_template('job.html', title='Job Details', job=job)

@app.route('/add_practices', methods=['GET', 'POST'])
@login_required
def add_practices():
    if not current_user.is_admin:
        flash('Only administrators can add practices.')
        return redirect(url_for('index'))
    form = PracticeForm()
    if form.validate_on_submit():
        practices = [Practice(name=name.strip()) for name in form.practice_names.data.split(',')]
        db.session.bulk_save_objects(practices)
        db.session.commit()
        flash('Practices added successfully!')
        return redirect(url_for('index'))
    return render_template('add_practices.html', title='Add Practices', form=form)

@app.route('/add_doctors', methods=['GET', 'POST'])
@login_required
def add_doctors():
    if not current_user.is_admin:
        flash('Only administrators can add doctors.')
        return redirect(url_for('index'))
    form = DoctorForm()
    if form.validate_on_submit():
        doctors = [Doctor(name=name.strip(), practice_id=form.practice_id.data) for name in form.doctor_names.data.split(',')]
        db.session.bulk_save_objects(doctors)
        db.session.commit()
        flash('Doctors added successfully!')
        return redirect(url_for('index'))
    return render_template('add_doctors.html', title='Add Doctors', form=form)

@app.route('/delete_job/<int:id>', methods=['POST'])
@login_required
def delete_job(id):
    if not current_user.is_admin:
        flash('Admin access required to delete jobs.')
        return redirect(url_for('index'))
        
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('index'))