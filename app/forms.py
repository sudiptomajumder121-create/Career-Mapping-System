from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, IntegerField, TextAreaField
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    usertype = SelectField('Select Usertype',
                           choices=[('Job Seeker', 'Job Seeker'),
                                    ('Company', 'Company')],
                           validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    phone_number = StringField('Phone Number')
    roll_number = StringField('Roll Number')
    college = StringField('College / University')
    degree_course = StringField('Degree / Course')
    skills = SelectMultipleField('Skills', choices=[('Python', 'Python'), ('Java', 'Java'), ('JavaScript', 'JavaScript'), ('HTML/CSS', 'HTML/CSS'), ('SQL', 'SQL'), ('React', 'React'), ('Node.js', 'Node.js'), ('AWS', 'AWS'), ('Docker', 'Docker'), ('Machine Learning', 'Machine Learning'), ('Cyber Security', 'Cyber Security'), ('UI/UX Design', 'UI/UX Design')], option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    skills_custom = StringField('Other Skills', description='Separate additional skills with commas')
    programming_languages = SelectMultipleField('Programming Languages', choices=[('Python', 'Python'), ('Java', 'Java'), ('JavaScript', 'JavaScript'), ('C++', 'C++'), ('C#', 'C#'), ('HTML/CSS', 'HTML/CSS'), ('SQL', 'SQL'), ('Swift', 'Swift')], option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    areas_of_interest = SelectMultipleField('Areas of Interest', choices=[('Web Development', 'Web Development'), ('Software Engineering', 'Software Engineering'), ('Data Analytics', 'Data Analytics'), ('Data Science', 'Data Science'), ('AI/ML', 'AI/ML'), ('Cyber Security', 'Cyber Security'), ('Cloud Computing', 'Cloud Computing'), ('DevOps', 'DevOps'), ('UI/UX Design', 'UI/UX Design'), ('Mobile App Development', 'Mobile App Development')], option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    preferred_career_field = SelectField('Preferred Career Field', choices=[('', 'Select a field'), ('Software Engineering', 'Software Engineering'), ('Web Development', 'Web Development'), ('Data Science', 'Data Science'), ('AI/ML', 'AI/ML'), ('Cyber Security', 'Cyber Security'), ('Cloud Computing', 'Cloud Computing'), ('DevOps', 'DevOps'), ('UI/UX Design', 'UI/UX Design'), ('Mobile App Development', 'Mobile App Development')])
    preferred_job_location = SelectField('Preferred Job Location', choices=[('', 'Any location'), ('Bengaluru', 'Bengaluru'), ('Hyderabad', 'Hyderabad'), ('Pune', 'Pune'), ('Mumbai', 'Mumbai'), ('Chennai', 'Chennai'), ('Gurugram', 'Gurugram'), ('Remote', 'Remote')])
    experience_level = SelectField('Experience Level', choices=[('Fresher', 'Fresher'), ('1-2 Years', '1-2 Years'), ('3+ Years', '3+ Years')])
    resume = FileField('Resume Upload (optional)', validators=[FileAllowed(['pdf', 'doc', 'docx'], 'Please upload a PDF, DOC, or DOCX file.')])
    submit = SubmitField('Sign Up')

    def validate_full_name(self, full_name):
        user = User.query.filter_by(username=full_name.data.strip()).first()
        if user:
            raise ValidationError('An account with that full name already exists. Please use your name as registered.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')

    def validate_roll_number(self, roll_number):
        if roll_number.data and User.query.filter_by(roll_number=roll_number.data.strip()).first():
            raise ValidationError('That roll number is already registered.')


class CandidateProfileForm(RegistrationForm):
    """The post-login profile editor reuses the candidate registration fields."""
    usertype = SelectField('Select Usertype', choices=[('Job Seeker', 'Job Seeker')])
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Save Profile & See Recommendations')

    def validate_full_name(self, full_name):
        return

    def validate_email(self, email):
        return

    def validate_roll_number(self, roll_number):
        return


class LoginForm(FlaskForm):
    usertype = SelectField('Select Usertype',
                           choices=[('Job Seeker', 'Job Seeker'),
                                    ('Company', 'Company')],
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ReviewForm(FlaskForm):
    username = StringField('Name',
                           validators=[DataRequired()])
    review = TextAreaField('Review',
                           validators=[DataRequired()])
    submit = SubmitField('Submit Review')


class JobForm(FlaskForm):
    title = StringField('Job Title',
                        validators=[DataRequired(), Length(min=2, max=20)])
    industry = SelectField('Industry', choices=[('Construction', 'Construction'),
                                                ('Education', 'Education'),
                                                ('Food And Beverage', 'Food and Beverage'),
                                                ('Pharmaceutical', 'Pharmaceutical'),
                                                ('Entertainment', 'Entertainment'),
                                                ('Manufacturing', 'Manufacturing'),
                                                ('Telecommunication', 'Telecommunication'),
                                                ('Agriculture', 'Agriculture'),
                                                ('Transportation', 'Transportation'),
                                                ('Computer And Technology', 'Computer and Technology'),
                                                ('Healthcare', 'Healthcare'),
                                                ('Media And News', 'Media and News'),
                                                ('Hospitality', 'Hospitality'),
                                                ('Energy', 'Energy'),
                                                ('Fashion', 'Fashion'),
                                                ('Telecommunication', 'Telecommunication'),
                                                ('Finance And Economic', 'Finance and Economic'),
                                                ('Advertising And Marketing', 'Advertising and Marketing'),
                                                ('Mining', 'Mining'),
                                                ('Aerospace', 'Aerospace')],
                           validators=[DataRequired()])
    description = TextAreaField('Job Description',
                                validators=[DataRequired()])
    submit = SubmitField('Submit')


class ApplicationForm(FlaskForm):
    gender = SelectField('Gender', choices=[('Male', 'Male'),
                                            ('Female', 'Female'),
                                            ('Others', 'Other')],
                         default='male',
                         validators=[DataRequired()])
    degree = SelectField('Degree',
                         default='eSchool',
                         choices=[('eSchool', 'School'),
                                  ('dHighSchool', 'HighSchool'),
                                  ('cBachelor', 'Bachelor'),
                                  ('bMaster', 'Master'),
                                  ('aPHD', 'PHD')],
                         validators=[DataRequired()])
    industry = SelectField('Industry',
                           default='Construction',
                           choices=[('Construction', 'Construction'),
                                    ('Education', 'Education'),
                                    ('Food And Beverage', 'Food and Beverage'),
                                    ('Pharmaceutical', 'Pharmaceutical'),
                                    ('Entertainment', 'Entertainment'),
                                    ('Manufacturing', 'Manufacturing'),
                                    ('Telecommunication', 'Telecommunication'),
                                    ('Agriculture', 'Agriculture'),
                                    ('Transportation', 'Transportation'),
                                    ('Computer And Technology', 'Computer and Technology'),
                                    ('Healthcare', 'Healthcare'),
                                    ('Media And News', 'Media and News'),
                                    ('Hospitality', 'Hospitality'),
                                    ('Energy', 'Energy'),
                                    ('Fashion', 'Fashion'),
                                    ('Telecommunication', 'Telecommunication'),
                                    ('Finance and Economic', 'Finance and Economic'),
                                    ('Advertising And Marketing', 'Advertising and Marketing'),
                                    ('Mining', 'Mining'),
                                    ('Aerospace', 'Aerospace')],
                           validators=[DataRequired()])
    experience = IntegerField('Professional Experience in years',
                              validators=[DataRequired()])
    cv = FileField('Update Resume', validators=[FileAllowed(['jpg', 'png', 'bmp', 'pdf'])])
    cover_letter = TextAreaField('Cover Letter',
                                 validators=[DataRequired()])
    submit = SubmitField('Submit')
