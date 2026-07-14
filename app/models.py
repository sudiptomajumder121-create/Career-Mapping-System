from app import db, login_manager
from datetime import date
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    usertype = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    full_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(25))
    roll_number = db.Column(db.String(60), unique=True)
    college = db.Column(db.String(150))
    degree_course = db.Column(db.String(100))
    skills = db.Column(db.Text)
    programming_languages = db.Column(db.Text)
    areas_of_interest = db.Column(db.Text)
    preferred_career_field = db.Column(db.String(100))
    preferred_job_location = db.Column(db.String(100))
    experience_level = db.Column(db.String(30))
    resume_filename = db.Column(db.String(255))
    company_name = db.Column(db.String(150))
    company_role = db.Column(db.String(100))
    company_job_title = db.Column(db.String(100))
    company_job_description = db.Column(db.Text)
    company_skills = db.Column(db.Text)
    company_interests = db.Column(db.Text)
    jobs = db.relationship('Jobs', backref='job_applier', lazy=True)
    applications = db.relationship('Application', backref='application_submiter', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.usertype}', '{self.email}')"


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=date.today())
    degree = db.Column(db.String(20), nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    cv = db.Column(db.String(20), nullable=False)
    cover_letter = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)


    def __repr__(self):
        return f"Application('{self.id}','{self.gender}', '{self.date_posted}', '{self.degree}', '{self.industry}', '{self.experience}', '{self.user_id}', '{self.job_id}')"

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(100))
    company_logo = db.Column(db.String(20))
    required_skills = db.Column(db.Text)
    experience_required = db.Column(db.String(50))
    location = db.Column(db.String(100))
    salary = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime, nullable=False, default=date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    applications = db.relationship('Application', backref='application_jober', lazy=True)



    def __repr__(self):
        return f"Jobs('{self.id}','{self.title}', '{self.industry}', '{self.date_posted}')"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    review = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Review('{self.username}', '{self.review}')"


class SurveyResponse(db.Model):
    """A student's professional-development interests from the survey export."""
    id = db.Column(db.Integer, primary_key=True)
    submitted_at = db.Column(db.DateTime, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), nullable=False, unique=True)
    course = db.Column(db.String(50), nullable=False)
    programming_languages = db.Column(db.Text, nullable=False)
    career_fields = db.Column(db.Text, nullable=False)
    other_skills = db.Column(db.Text, nullable=False)
    dream_companies = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"SurveyResponse('{self.name}', '{self.roll_number}')"
