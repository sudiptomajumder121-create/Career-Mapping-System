import re


def tokens(value):
    """Normalize comma-separated profile/job data into comparable skill tokens."""
    return {item.strip().lower() for item in re.split(r'[,/;|]+', value or '') if item.strip()}


def job_match_score(user, job):
    """Return the percentage of required skills present in the candidate profile."""
    required = tokens(job.required_skills)
    candidate = tokens(','.join(filter(None, [user.skills, user.programming_languages])))
    if not required or not candidate:
        return 0
    return round(len(required & candidate) / len(required) * 100)


def has_skill_match(user, job):
    """Recommendations require at least one direct candidate/job-skill overlap."""
    required = tokens(job.required_skills)
    candidate = tokens(','.join(filter(None, [user.skills, user.programming_languages])))
    return bool(required & candidate)


def ranked_jobs(user, jobs):
    matches = [(job, job_match_score(user, job)) for job in jobs]
    return sorted(matches, key=lambda item: item[1], reverse=True)
