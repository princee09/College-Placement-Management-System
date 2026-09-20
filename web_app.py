"""Browser dashboard for the College Placement Management System."""
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from pymongo.errors import DuplicateKeyError, WriteError
from database.connection import get_database
from operations.reports import placement_report

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-before-production"

COLLECTIONS = {
    "students": {"label": "Students", "id": "student_id", "fields": [("student_id", "Student ID", "text"), ("name", "Full name", "text"), ("email", "Email", "email"), ("phone", "Phone", "text"), ("department", "Department", "text"), ("year", "Year", "number"), ("cgpa", "CGPA", "number"), ("skills", "Skills (comma separated)", "text")]},
    "companies": {"label": "Companies", "id": "company_id", "fields": [("company_id", "Company ID", "text"), ("name", "Company name", "text"), ("industry", "Industry", "text"), ("location", "Location", "text"), ("website", "Website", "url")]},
    "jobs": {"label": "Jobs", "id": "job_id", "fields": [("job_id", "Job ID", "text"), ("company_id", "Company ID", "text"), ("title", "Job title", "text"), ("package_lpa", "Package (LPA)", "number"), ("location", "Location", "text"), ("skills_required", "Required skills (comma separated)", "text"), ("vacancies", "Vacancies", "number"), ("status", "Status", "text")]},
    "applications": {"label": "Applications", "id": "application_id", "fields": [("application_id", "Application ID", "text"), ("student_id", "Student ID", "text"), ("job_id", "Job ID", "text"), ("application_date", "Application date", "date"), ("status", "Status", "text")]},
    "interviews": {"label": "Interviews", "id": "interview_id", "fields": [("interview_id", "Interview ID", "text"), ("application_id", "Application ID", "text"), ("round", "Interview round", "text"), ("interview_date", "Interview date", "date"), ("result", "Result", "text")]},
    "placements": {"label": "Placements", "id": "placement_id", "fields": [("placement_id", "Placement ID", "text"), ("student_id", "Student ID", "text"), ("company_id", "Company ID", "text"), ("job_id", "Job ID", "text"), ("package_lpa", "Package (LPA)", "number"), ("placement_date", "Placement date", "date"), ("status", "Status", "text")]},
}


def normalise_document(collection, form):
    document = {key: form.get(key, "").strip() for key, _, _ in COLLECTIONS[collection]["fields"]}
    for key in ("year", "vacancies"):
        if key in document: document[key] = int(document[key])
    for key in ("cgpa", "package_lpa"):
        if key in document: document[key] = float(document[key])
    for key in ("skills", "skills_required"):
        if key in document: document[key] = [item.strip() for item in document[key].split(",") if item.strip()]
    for key in ("application_date", "interview_date", "placement_date"):
        if key in document: document[key] = datetime.strptime(document[key], "%Y-%m-%d")
    return document


@app.context_processor
def inject_navigation(): return {"navigation": COLLECTIONS}


@app.get("/")
def dashboard():
    db = get_database()
    report = placement_report(db)
    jobs = list(db.jobs.find({}, {"_id": 0}).sort("package_lpa", -1).limit(5))
    statuses = list(db.applications.aggregate([{"$group": {"_id": "$status", "total": {"$sum": 1}}}]))
    return render_template("dashboard.html", report=report, jobs=jobs, statuses=statuses)


@app.get("/<collection>")
def records(collection):
    if collection not in COLLECTIONS: return redirect(url_for("dashboard"))
    config = COLLECTIONS[collection]
    rows = list(get_database()[collection].find({}, {"_id": 0}).sort(config["id"], 1))
    return render_template("records.html", collection=collection, config=config, rows=rows)


@app.post("/<collection>/add")
def add_record(collection):
    if collection not in COLLECTIONS: return redirect(url_for("dashboard"))
    try:
        get_database()[collection].insert_one(normalise_document(collection, request.form))
        flash("Record added successfully.", "success")
    except (ValueError, DuplicateKeyError, WriteError) as error:
        flash(f"Could not save record: {error}", "error")
    return redirect(url_for("records", collection=collection))


@app.post("/<collection>/<record_id>/delete")
def delete_record(collection, record_id):
    if collection not in COLLECTIONS: return redirect(url_for("dashboard"))
    result = get_database()[collection].delete_one({COLLECTIONS[collection]["id"]: record_id})
    flash("Record deleted." if result.deleted_count else "Record not found.", "success" if result.deleted_count else "error")
    return redirect(url_for("records", collection=collection))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
