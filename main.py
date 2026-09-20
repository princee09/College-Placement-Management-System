"""Menu-driven College Placement Management System using PyMongo."""
from datetime import datetime
from pprint import pprint
from pymongo.errors import DuplicateKeyError, WriteError
from database.connection import get_database
from operations.reports import print_aggregation_examples, print_report


MENU = """
COLLEGE PLACEMENT MANAGEMENT SYSTEM
1. Add Student                 8. View Jobs
2. View Students               9. Apply for Job
3. Update Student             10. View Applications
4. Delete Student             11. Schedule Interview
5. Add Company                12. Add Placement
6. View Companies             13. Generate Placement Report
7. Add Job                    14. Run Aggregation Examples
0. Exit
"""


def ask_date(prompt):
    return datetime.strptime(input(prompt).strip(), "%Y-%m-%d")


def show_documents(cursor):
    found = False
    for document in cursor:
        document.pop("_id", None)
        pprint(document, sort_dicts=False)
        found = True
    if not found:
        print("No records found.")


def add_student(db):
    document = {
        "student_id": input("Student ID: ").strip(), "name": input("Name: ").strip(),
        "email": input("Email: ").strip(), "phone": input("Phone: ").strip(),
        "department": input("Department: ").strip(), "year": int(input("Year (1-4): ")),
        "cgpa": float(input("CGPA (0-10): ")), "skills": [s.strip() for s in input("Skills (comma-separated): ").split(",") if s.strip()],
    }
    db.students.insert_one(document)
    print("Student added successfully.")


def update_student(db):
    student_id = input("Student ID: ").strip()
    cgpa = float(input("New CGPA (0-10): "))
    result = db.students.update_one({"student_id": student_id}, {"$set": {"cgpa": cgpa}})
    print("Student updated." if result.matched_count else "Student ID not found.")


def delete_student(db):
    student_id = input("Student ID: ").strip()
    if db.applications.count_documents({"student_id": student_id}):
        print("Cannot delete: this student has job applications. Delete related records first.")
        return
    result = db.students.delete_one({"student_id": student_id})
    print("Student deleted." if result.deleted_count else "Student ID not found.")


def add_company(db):
    db.companies.insert_one({"company_id": input("Company ID: ").strip(), "name": input("Company name: ").strip(), "industry": input("Industry: ").strip(), "location": input("Location: ").strip(), "website": input("Website: ").strip()})
    print("Company added successfully.")


def add_job(db):
    company_id = input("Company ID: ").strip()
    if not db.companies.find_one({"company_id": company_id}):
        print("Company ID does not exist.")
        return
    db.jobs.insert_one({"job_id": input("Job ID: ").strip(), "company_id": company_id, "title": input("Title: ").strip(), "package_lpa": float(input("Package (LPA): ")), "location": input("Location: ").strip(), "skills_required": [s.strip() for s in input("Required skills (comma-separated): ").split(",") if s.strip()], "vacancies": int(input("Vacancies: ")), "status": "Open"})
    print("Job added successfully.")


def apply_for_job(db):
    student_id, job_id = input("Student ID: ").strip(), input("Job ID: ").strip()
    if not db.students.find_one({"student_id": student_id}) or not db.jobs.find_one({"job_id": job_id, "status": "Open"}):
        print("Use an existing student and an open job.")
        return
    db.applications.insert_one({"application_id": input("Application ID: ").strip(), "student_id": student_id, "job_id": job_id, "application_date": datetime.now(), "status": "Applied"})
    print("Application created successfully.")


def schedule_interview(db):
    application_id = input("Application ID: ").strip()
    if not db.applications.find_one({"application_id": application_id}):
        print("Application ID does not exist.")
        return
    db.interviews.insert_one({"interview_id": input("Interview ID: ").strip(), "application_id": application_id, "round": input("Round: ").strip(), "interview_date": ask_date("Interview date (YYYY-MM-DD): "), "result": "Scheduled"})
    print("Interview scheduled successfully.")


def add_placement(db):
    student_id, job_id = input("Student ID: ").strip(), input("Job ID: ").strip()
    job = db.jobs.find_one({"job_id": job_id})
    if not job or not db.students.find_one({"student_id": student_id}):
        print("Use existing student and job IDs.")
        return
    db.placements.insert_one({"placement_id": input("Placement ID: ").strip(), "student_id": student_id, "company_id": job["company_id"], "job_id": job_id, "package_lpa": job["package_lpa"], "placement_date": datetime.now(), "status": "Placed"})
    db.applications.update_many({"student_id": student_id, "job_id": job_id}, {"$set": {"status": "Selected"}})
    print("Placement recorded successfully.")


def run(db):
    actions = {
        "1": lambda: add_student(db), "2": lambda: show_documents(db.students.find()), "3": lambda: update_student(db), "4": lambda: delete_student(db),
        "5": lambda: add_company(db), "6": lambda: show_documents(db.companies.find()), "7": lambda: add_job(db), "8": lambda: show_documents(db.jobs.find().sort("package_lpa", -1)),
        "9": lambda: apply_for_job(db), "10": lambda: show_documents(db.applications.find()), "11": lambda: schedule_interview(db), "12": lambda: add_placement(db),
        "13": lambda: print_report(db), "14": lambda: print_aggregation_examples(db),
    }
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            return
        try:
            action = actions.get(choice)
            print("Invalid option." if action is None else "")
            if action:
                action()
        except (ValueError, DuplicateKeyError, WriteError) as error:
            print(f"Operation failed: {error}")


if __name__ == "__main__":
    try:
        run(get_database())
    except RuntimeError as error:
        print(error)
