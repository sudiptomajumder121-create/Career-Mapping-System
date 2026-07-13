"""Add Career Mapping System columns to an existing SQLite database safely."""
from app import app, db


USER_COLUMNS = {
    'full_name': 'VARCHAR(100)', 'phone_number': 'VARCHAR(25)', 'roll_number': 'VARCHAR(60)',
    'college': 'VARCHAR(150)', 'degree_course': 'VARCHAR(100)', 'skills': 'TEXT',
    'programming_languages': 'TEXT', 'areas_of_interest': 'TEXT',
    'preferred_career_field': 'VARCHAR(100)', 'preferred_job_location': 'VARCHAR(100)',
    'experience_level': 'VARCHAR(30)', 'resume_filename': 'VARCHAR(255)',
}
JOB_COLUMNS = {
    'company': 'VARCHAR(100)', 'company_logo': 'VARCHAR(20)', 'required_skills': 'TEXT',
    'experience_required': 'VARCHAR(50)', 'location': 'VARCHAR(100)', 'salary': 'VARCHAR(100)',
}


def add_missing_columns(table, columns):
    existing = {column['name'] for column in db.inspect(db.engine).get_columns(table)}
    for name, sql_type in columns.items():
        if name not in existing:
            db.session.execute(f'ALTER TABLE {table} ADD COLUMN {name} {sql_type}')


with app.app_context():
    db.create_all()
    add_missing_columns('user', USER_COLUMNS)
    add_missing_columns('jobs', JOB_COLUMNS)
    db.session.commit()
    print('Database schema is ready for Career Mapping System.')
