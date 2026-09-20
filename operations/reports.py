"""Aggregation pipelines for placement insights."""


def placement_report(db):
    """Calculate all report values from live MongoDB data."""
    highest = list(db.placements.aggregate([{"$group": {"_id": None, "highest": {"$max": "$package_lpa"}}}]))
    average = list(db.jobs.aggregate([{"$group": {"_id": None, "average": {"$avg": "$package_lpa"}}}]))
    hiring_company = list(db.placements.aggregate([
        {"$group": {"_id": "$company_id", "placements": {"$sum": 1}}}, {"$sort": {"placements": -1}}, {"$limit": 1},
        {"$lookup": {"from": "companies", "localField": "_id", "foreignField": "company_id", "as": "company"}},
        {"$unwind": "$company"}, {"$project": {"_id": 0, "name": "$company.name", "placements": 1}},
    ]))
    applied_job = list(db.applications.aggregate([
        {"$group": {"_id": "$job_id", "applications": {"$sum": 1}}}, {"$sort": {"applications": -1}}, {"$limit": 1},
        {"$lookup": {"from": "jobs", "localField": "_id", "foreignField": "job_id", "as": "job"}},
        {"$unwind": "$job"}, {"$project": {"_id": 0, "title": "$job.title", "applications": 1}},
    ]))
    return {
        "Total Students": db.students.count_documents({}), "Total Companies": db.companies.count_documents({}),
        "Total Jobs": db.jobs.count_documents({}), "Total Applications": db.applications.count_documents({}),
        "Total Selected": db.applications.count_documents({"status": "Selected"}),
        "Average Package (LPA)": round(average[0]["average"], 2) if average else 0,
        "Highest Package (LPA)": highest[0]["highest"] if highest else 0,
        "Top Hiring Company": hiring_company[0]["name"] if hiring_company else "N/A",
        "Most Applied Job": applied_job[0]["title"] if applied_job else "N/A",
    }


def print_report(db):
    report = placement_report(db)
    print("\n========== PLACEMENT REPORT ==========")
    for label, value in report.items():
        print(f"{label:<25}: {value}")
    print("======================================")


def print_aggregation_examples(db):
    """Show required aggregation pipelines and their actual output."""
    examples = {
        "Applications by status": [{"$group": {"_id": "$status", "total": {"$sum": 1}}}, {"$sort": {"_id": 1}}],
        "Students by department": [{"$group": {"_id": "$department", "total_students": {"$sum": 1}}}, {"$sort": {"_id": 1}}],
        "Top 5 paying jobs": [{"$sort": {"package_lpa": -1}}, {"$limit": 5}, {"$project": {"_id": 0, "job_id": 1, "title": 1, "package_lpa": 1}}],
        "Application with student information": [
            {"$lookup": {"from": "students", "localField": "student_id", "foreignField": "student_id", "as": "student"}},
            {"$unwind": "$student"}, {"$project": {"_id": 0, "application_id": 1, "status": 1, "student.name": 1, "student.department": 1, "student.cgpa": 1}},
        ],
    }
    collections = {"Applications by status": db.applications, "Students by department": db.students, "Top 5 paying jobs": db.jobs, "Application with student information": db.applications}
    for title, pipeline in examples.items():
        print(f"\n{title}:")
        for row in collections[title].aggregate(pipeline):
            print(row)
