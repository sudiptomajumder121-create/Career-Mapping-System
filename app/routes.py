from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from PIL import Image
import os
import secrets
from app.forms import RegistrationForm, CandidateProfileForm, LoginForm, ReviewForm, JobForm, ApplicationForm
from app.models import User, Jobs, Review, Application, SurveyResponse
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app.matching import ranked_jobs, has_skill_match
import random

rev = [
    {
        'username': 'Jeff Bezos',
        'review': 'I hired multiple people using this website. Thank you'
    },
    {
        'username': 'Tim David',
        'review': 'The website helped me to get placed! Seemless experience'
    },
    {
        'username': 'Larry Page',
        'review': 'Best website ever'
    }
]


# Flask-SQLAlchemy 3 requires an active application context for queries.  Keep
# the existing sample-review fallback available during module import; database
# review queries happen only from request handlers.
Random_Review = rev


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.usertype == 'Job Seeker':
            return redirect(url_for('show_jobs'))
        elif current_user.usertype == 'Company':
            return redirect(url_for('posted_jobs'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.full_name.data.strip(), full_name=form.full_name.data.strip(),
                    usertype=form.usertype.data, email=form.email.data, password=hashed_password)
        update_candidate_profile(user, form)
        db.session.add(user)
        db.session.commit()
        flash('You account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, Random_Review=Random_Review)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.usertype == 'Job Seeker':
            return redirect(url_for('show_jobs'))
        elif current_user.usertype == 'Company':
            return redirect(url_for('posted_jobs'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print('password clear')
            if form.usertype.data == user.usertype and form.usertype.data == 'Company':
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('posted_jobs'))
            elif form.usertype.data == user.usertype and form.usertype.data == 'Job Seeker':
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('recommended_jobs') if user.skills else url_for('candidate_profile'))
            else:
                flash('Login Unsuccessful. Please check email, password and usertype', 'danger')
        else:
            flash('Login Unsuccessful. Please check email, password and usertype', 'danger')
            return render_template('login.html', form=form, Random_Review=Random_Review)
    return render_template('login.html', form=form, Random_Review=Random_Review)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('show_jobs'))

def save_picture(form_picture):
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f_name + f_ext
    picture_path = os.path.join(app.root_path, 'static', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


def save_resume(resume):
    filename = secure_filename(resume.filename)
    filename = f"{secrets.token_hex(8)}_{filename}"
    resume.save(os.path.join(app.root_path, 'static', filename))
    return filename


def selected_values(field):
    return ', '.join(field.data or [])


def update_candidate_profile(user, form):
    """Persist registration/profile fields while leaving company accounts lightweight."""
    if user.usertype != 'Job Seeker':
        return
    base_skills = selected_values(form.skills)
    custom_skills = (form.skills_custom.data or '').strip()
    user.phone_number = (form.phone_number.data or '').strip()
    user.roll_number = (form.roll_number.data or '').strip() or None
    user.college = (form.college.data or '').strip()
    user.degree_course = (form.degree_course.data or '').strip()
    user.skills = ', '.join(filter(None, [base_skills, custom_skills]))
    user.programming_languages = selected_values(form.programming_languages)
    user.areas_of_interest = selected_values(form.areas_of_interest)
    user.preferred_career_field = form.preferred_career_field.data or None
    user.preferred_job_location = form.preferred_job_location.data or None
    user.experience_level = form.experience_level.data or None
    if form.resume.data:
        user.resume_filename = save_resume(form.resume.data)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def candidate_profile():
    if current_user.usertype != 'Job Seeker':
        flash('Candidate profiles are available to job seekers.', 'info')
        return redirect(url_for('show_jobs'))
    form = CandidateProfileForm()
    # The profile screen is job-seeker-only and intentionally does not expose an account-type selector.
    if request.method == 'POST':
        form.usertype.data = 'Job Seeker'
    if request.method == 'GET':
        form.full_name.data = current_user.full_name or current_user.username
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.roll_number.data = current_user.roll_number
        form.college.data = current_user.college
        form.degree_course.data = current_user.degree_course
        form.skills.data = [item.strip() for item in (current_user.skills or '').split(',') if item.strip() in dict(form.skills.choices)]
        form.programming_languages.data = [item.strip() for item in (current_user.programming_languages or '').split(',') if item.strip() in dict(form.programming_languages.choices)]
        form.areas_of_interest.data = [item.strip() for item in (current_user.areas_of_interest or '').split(',') if item.strip() in dict(form.areas_of_interest.choices)]
        form.preferred_career_field.data = current_user.preferred_career_field
        form.preferred_job_location.data = current_user.preferred_job_location
        form.experience_level.data = current_user.experience_level or 'Fresher'
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data.strip()
        current_user.username = form.full_name.data.strip()
        current_user.email = form.email.data
        update_candidate_profile(current_user, form)
        db.session.commit()
        flash('Profile saved. Your recommendations are ready!', 'success')
        return redirect(url_for('recommended_jobs'))
    return render_template('profile.html', form=form, Random_Review=Random_Review)

@app.route("/post_cvs/<jobid>", methods=['GET', 'POST'])
@login_required
def post_cvs(jobid):
    form = ApplicationForm()
    job = Jobs.query.filter_by(id=jobid).first()
    if form.validate_on_submit():
        application = Application(gender=form.gender.data,
                              degree=form.degree.data,
                              industry=form.industry.data,
                              experience=form.experience.data,
                              cover_letter=form.cover_letter.data,
                              application_submiter=current_user,
                              application_jober=job,
                              cv=form.cv.data.filename)
        print(form.cv.data)
        picture_file = save_picture(form.cv.data)
        db.session.add(application)
        db.session.commit()
        return redirect(url_for('show_jobs'))
    return render_template('post_cvs.html', form=form, Random_Review=Random_Review)

@app.route("/post_jobs", methods=['GET', 'POST'])
@login_required
def post_jobs():
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(title=form.title.data,
                   industry=form.industry.data,
                   description=form.description.data,
                   job_applier=current_user)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('posted_jobs'))
    return render_template('post_jobs.html', form=form, Random_Review=Random_Review)


@app.route("/review", methods=['GET', 'POST'])
@login_required
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(username=form.username.data,
                            review=form.review.data)
        db.session.add(review)
        db.session.commit()
        flash('Thank you for providing the review!', 'success')
        return redirect(url_for('show_jobs'))
    return  render_template('review.html', form=form, Random_Review=Random_Review)

@app.route("/posted_jobs")
@login_required
def posted_jobs():
    jobs = Jobs.query.filter_by(job_applier=current_user).all()
    return render_template('all_jobs.html', job_cards=[{'job': job, 'score': None} for job in jobs],
                           Random_Review=Random_Review,
                           filters={'title': '', 'company': '', 'skill': '', 'location': '', 'experience': ''},
                           companies=[], locations=[], experiences=[])


@app.route("/show_applications/<jobid>", methods=['GET'])
@login_required
def show_applications(jobid):
    applications = Application.query.filter_by(job_id=jobid).order_by(Application.degree, Application.experience.desc()).all()
    return render_template('show_applications.html', applications=applications, Random_Review=Random_Review)


@app.route("/professional-development-survey")
@login_required
def professional_development_survey():
    responses = SurveyResponse.query.order_by(SurveyResponse.submitted_at.desc()).all()
    return render_template('professional_development_survey.html', responses=responses,
                           Random_Review=Random_Review)

@app.route("/meeting/<application_id>")
@login_required
def meeting(application_id):
    applicant_id = Application.query.get(int(application_id)).user_id
    applicant = User.query.get(applicant_id)
    return render_template('meeting.html', applicant=applicant, Random_Review=Random_Review)


@app.route('/recommended-jobs')
@login_required
def recommended_jobs():
    if current_user.usertype != 'Job Seeker':
        return redirect(url_for('show_jobs'))
    if not current_user.skills and not current_user.programming_languages:
        flash('Complete your profile to receive tailored recommendations.', 'info')
        return redirect(url_for('candidate_profile'))
    matches = ranked_jobs(current_user, Jobs.query.all())
    job_cards = [{'job': job, 'score': score} for job, score in matches
                 if has_skill_match(current_user, job)][:5]
    return render_template('recommended_jobs.html', job_cards=job_cards, Random_Review=Random_Review)

@app.route("/")
@app.route("/show_jobs")
@app.route('/all-jobs')
def show_jobs():
    filters = {
        'title': request.args.get('title', '').strip(),
        'company': request.args.get('company', '').strip(),
        'skill': request.args.get('skill', '').strip(),
        'location': request.args.get('location', '').strip(),
        'experience': request.args.get('experience', '').strip(),
    }
    jobs = Jobs.query.all()
    if current_user.is_authenticated and current_user.usertype == 'Job Seeker' and (current_user.skills or current_user.programming_languages):
        matches = ranked_jobs(current_user, jobs)
        job_cards = [{'job': job, 'score': score} for job, score in matches]
    else:
        job_cards = [{'job': job, 'score': None} for job in jobs]
    def matches_filters(card):
        job = card['job']
        return (
            (not filters['title'] or filters['title'].lower() in (job.title or '').lower()) and
            (not filters['company'] or filters['company'].lower() in (job.company or '').lower()) and
            (not filters['skill'] or filters['skill'].lower() in (job.required_skills or '').lower()) and
            (not filters['location'] or filters['location'].lower() in (job.location or '').lower()) and
            (not filters['experience'] or filters['experience'].lower() in (job.experience_required or '').lower())
        )
    job_cards = [card for card in job_cards if matches_filters(card)]
    companies = sorted({job.company for job in Jobs.query.all() if job.company})
    locations = sorted({job.location for job in Jobs.query.all() if job.location})
    experiences = sorted({job.experience_required for job in Jobs.query.all() if job.experience_required})
    return render_template('all_jobs.html', job_cards=job_cards, Random_Review=Random_Review,
                           filters=filters, companies=companies, locations=locations, experiences=experiences)

@app.route("/resume/<id>", methods=['GET'])
def resume(id):
    cv = Application.query.get(int(id)).cv
    return render_template('resume.html', cv=cv, Random_Review=Random_Review, id=id)
