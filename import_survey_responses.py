"""Import the Professional Development Interest Survey CSV into site.db.

Usage:
    python3 import_survey_responses.py /path/to/Form\ Responses\ 1.csv
"""
import csv
import sys
from datetime import datetime
from pathlib import Path

from app import app, db
from app.models import SurveyResponse


EXPECTED_COLUMNS = 8


def import_responses(csv_path):
    with Path(csv_path).open(newline='', encoding='utf-8-sig') as source:
        rows = list(csv.reader(source))

    if not rows or len(rows[0]) != EXPECTED_COLUMNS:
        raise ValueError('The CSV must contain the eight survey-export columns.')

    added = updated = 0
    for row in rows[1:]:
        if not row:
            continue
        if len(row) != EXPECTED_COLUMNS:
            raise ValueError(f'Invalid row with {len(row)} columns: {row!r}')

        submitted_at = datetime.strptime(row[0].strip(), '%m/%d/%Y %H:%M:%S')
        values = {
            'submitted_at': submitted_at,
            'name': row[1].strip(),
            'roll_number': row[2].strip(),
            'course': row[3].strip(),
            'programming_languages': row[4].strip(),
            'career_fields': row[5].strip(),
            'other_skills': row[6].strip(),
            'dream_companies': row[7].strip(),
        }
        response = SurveyResponse.query.filter_by(roll_number=values['roll_number']).first()
        if response:
            for field, value in values.items():
                setattr(response, field, value)
            updated += 1
        else:
            db.session.add(SurveyResponse(**values))
            added += 1

    db.session.commit()
    return added, updated


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 import_survey_responses.py <survey.csv>')

    with app.app_context():
        db.create_all()
        added, updated = import_responses(sys.argv[1])
        print(f'Imported survey responses: {added} added, {updated} updated.')
