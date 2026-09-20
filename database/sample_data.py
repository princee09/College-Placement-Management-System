"""Realistic, idempotent sample data for demonstrations."""
from datetime import datetime

SAMPLE_DATA = {
    "students": [
        {"student_id": "STU001", "name": "Rahul Sharma", "email": "rahul.sharma@example.edu", "phone": "9876543210", "department": "CSE", "year": 4, "cgpa": 8.45, "skills": ["Python", "MongoDB", "Machine Learning"]},
        {"student_id": "STU002", "name": "Ananya Iyer", "email": "ananya.iyer@example.edu", "phone": "9876543211", "department": "ISE", "year": 4, "cgpa": 9.10, "skills": ["Java", "SQL", "React"]},
        {"student_id": "STU003", "name": "Vikram Singh", "email": "vikram.singh@example.edu", "phone": "9876543212", "department": "CSE", "year": 4, "cgpa": 7.90, "skills": ["Python", "Git", "Docker"]},
        {"student_id": "STU004", "name": "Meera Nair", "email": "meera.nair@example.edu", "phone": "9876543213", "department": "ECE", "year": 4, "cgpa": 8.20, "skills": ["C++", "IoT", "Python"]},
        {"student_id": "STU005", "name": "Arjun Das", "email": "arjun.das@example.edu", "phone": "9876543214", "department": "CSE", "year": 4, "cgpa": 8.75, "skills": ["Python", "MongoDB", "Git"]},
    ],
    "companies": [
        {"company_id": "COMP001", "name": "TechNova Solutions", "industry": "Information Technology", "location": "Bengaluru", "website": "https://technova.example"},
        {"company_id": "COMP002", "name": "DataSphere Analytics", "industry": "Analytics", "location": "Hyderabad", "website": "https://datasphere.example"},
        {"company_id": "COMP003", "name": "CloudAxis Systems", "industry": "Cloud Computing", "location": "Pune", "website": "https://cloudaxis.example"},
    ],
    "jobs": [
        {"job_id": "JOB001", "company_id": "COMP001", "title": "Software Developer", "package_lpa": 8.5, "location": "Bengaluru", "skills_required": ["Python", "MongoDB", "Git"], "vacancies": 10, "status": "Open"},
        {"job_id": "JOB002", "company_id": "COMP002", "title": "Data Analyst", "package_lpa": 7.2, "location": "Hyderabad", "skills_required": ["Python", "SQL"], "vacancies": 5, "status": "Open"},
        {"job_id": "JOB003", "company_id": "COMP003", "title": "Cloud Engineer", "package_lpa": 10.0, "location": "Pune", "skills_required": ["Docker", "Python", "AWS"], "vacancies": 4, "status": "Open"},
        {"job_id": "JOB004", "company_id": "COMP001", "title": "Frontend Developer", "package_lpa": 6.8, "location": "Bengaluru", "skills_required": ["React", "JavaScript"], "vacancies": 3, "status": "Closed"},
    ],
    "applications": [
        {"application_id": "APP001", "student_id": "STU001", "job_id": "JOB001", "application_date": datetime(2026, 9, 5), "status": "Selected"},
        {"application_id": "APP002", "student_id": "STU002", "job_id": "JOB002", "application_date": datetime(2026, 9, 6), "status": "Shortlisted"},
        {"application_id": "APP003", "student_id": "STU003", "job_id": "JOB003", "application_date": datetime(2026, 9, 7), "status": "Applied"},
        {"application_id": "APP004", "student_id": "STU004", "job_id": "JOB001", "application_date": datetime(2026, 9, 8), "status": "Rejected"},
        {"application_id": "APP005", "student_id": "STU005", "job_id": "JOB001", "application_date": datetime(2026, 9, 9), "status": "Selected"},
    ],
    "interviews": [
        {"interview_id": "INT001", "application_id": "APP001", "round": "Technical", "interview_date": datetime(2026, 9, 12), "result": "Passed"},
        {"interview_id": "INT002", "application_id": "APP002", "round": "Technical", "interview_date": datetime(2026, 9, 13), "result": "Scheduled"},
        {"interview_id": "INT003", "application_id": "APP004", "round": "HR", "interview_date": datetime(2026, 9, 14), "result": "Failed"},
        {"interview_id": "INT004", "application_id": "APP005", "round": "HR", "interview_date": datetime(2026, 9, 15), "result": "Passed"},
    ],
    "placements": [
        {"placement_id": "PLC001", "student_id": "STU001", "company_id": "COMP001", "job_id": "JOB001", "package_lpa": 8.5, "placement_date": datetime(2026, 9, 20), "status": "Placed"},
        {"placement_id": "PLC002", "student_id": "STU005", "company_id": "COMP001", "job_id": "JOB001", "package_lpa": 8.5, "placement_date": datetime(2026, 9, 21), "status": "Placed"},
    ],
}


def seed_database(db):
    """Upsert documents so re-running setup never duplicates the data."""
    id_fields = {"students": "student_id", "companies": "company_id", "jobs": "job_id", "applications": "application_id", "interviews": "interview_id", "placements": "placement_id"}
    for collection, documents in SAMPLE_DATA.items():
        identifier = id_fields[collection]
        for document in documents:
            db[collection].replace_one({identifier: document[identifier]}, document, upsert=True)
