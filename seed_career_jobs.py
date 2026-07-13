"""Replace the portal's sample job listings with realistic IT company openings."""
from app import app, db, bcrypt
from app.models import Application, Jobs, User


COMPANIES = {
    'Google': ('GO', 'Bengaluru', [('Software Engineer', 'Python, Java, Data Structures, Algorithms'), ('Data Scientist', 'Python, SQL, Machine Learning, Statistics'), ('Cloud Engineer', 'Google Cloud, Python, Docker, Kubernetes')]),
    'Microsoft': ('MS', 'Hyderabad', [('Backend Developer', 'C#, Python, SQL, REST APIs'), ('AI/ML Engineer', 'Python, Machine Learning, Azure, SQL'), ('Frontend Developer', 'JavaScript, React, HTML/CSS, TypeScript')]),
    'Amazon': ('AM', 'Bengaluru', [('Data Analyst', 'SQL, Python, Excel, Data Analytics'), ('DevOps Engineer', 'AWS, Docker, Kubernetes, Python'), ('Full Stack Developer', 'JavaScript, React, Node.js, SQL')]),
    'Apple': ('AP', 'Bengaluru', [('Mobile App Developer', 'Swift, iOS, REST APIs, Git'), ('Software Engineer', 'Python, Java, Data Structures, Algorithms'), ('UI/UX Designer', 'UI/UX Design, Figma, Prototyping, HTML/CSS')]),
    'IBM': ('IB', 'Pune', [('Java Developer', 'Java, Spring Boot, SQL, REST APIs'), ('Cyber Security Analyst', 'Cyber Security, Networking, Linux, Python'), ('Cloud Engineer', 'AWS, Azure, Docker, Kubernetes')]),
    'Infosys': ('IN', 'Pune', [('Python Developer', 'Python, Django, SQL, REST APIs'), ('Data Scientist', 'Python, SQL, Machine Learning, Statistics'), ('Frontend Developer', 'JavaScript, Angular, HTML/CSS, CSS')]),
    'TCS': ('TC', 'Chennai', [('Java Developer', 'Java, Spring Boot, SQL, Git'), ('Backend Developer', 'Python, Django, SQL, REST APIs'), ('Cyber Security Analyst', 'Cyber Security, Networking, Linux, SIEM')]),
    'Wipro': ('WI', 'Bengaluru', [('Cloud Engineer', 'AWS, Azure, Docker, Kubernetes'), ('Data Analyst', 'SQL, Python, Power BI, Data Analytics'), ('DevOps Engineer', 'Docker, Kubernetes, Jenkins, AWS')]),
    'Accenture': ('AC', 'Gurugram', [('Full Stack Developer', 'JavaScript, React, Node.js, SQL'), ('AI/ML Engineer', 'Python, Machine Learning, TensorFlow, SQL'), ('UI/UX Designer', 'UI/UX Design, Figma, Prototyping, User Research')]),
    'Capgemini': ('CG', 'Mumbai', [('Software Engineer', 'Java, Python, Data Structures, Git'), ('Backend Developer', 'Java, Spring Boot, SQL, REST APIs'), ('Mobile App Developer', 'JavaScript, React Native, REST APIs, Git')]),
}


def experience_for(title):
    return 'Fresher / 1–2 years' if title not in {'Data Scientist', 'AI/ML Engineer', 'DevOps Engineer'} else '1–3 years'


def salary_for(title):
    return '₹6–12 LPA' if title in {'Data Analyst', 'Frontend Developer', 'UI/UX Designer'} else '₹8–18 LPA'


with app.app_context():
    employer = User.query.filter_by(usertype='Company').first()
    if not employer:
        employer = User(username='Career Mapping Admin', full_name='Career Mapping Admin',
                        usertype='Company', email='admin@careermapping.local',
                        password=bcrypt.generate_password_hash('ChangeMe123!').decode('utf-8'))
        db.session.add(employer)
        db.session.flush()

    # The old portal listings are demonstration data; replace them with the requested IT openings.
    Application.query.delete()
    Jobs.query.delete()
    for company, (logo, location, openings) in COMPANIES.items():
        for title, required_skills in openings:
            description = (f'{company} is looking for a {title} to collaborate with cross-functional teams, '
                           f'deliver reliable technology solutions, and grow through mentorship.')
            db.session.add(Jobs(title=title, company=company, company_logo=logo,
                                industry='Information Technology', description=description,
                                required_skills=required_skills,
                                experience_required=experience_for(title), location=location,
                                salary=salary_for(title), job_applier=employer))
    db.session.commit()
    print(f'Seeded {Jobs.query.count()} jobs across {len(COMPANIES)} IT companies.')
