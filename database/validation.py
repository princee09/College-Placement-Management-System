"""Collection validators and indexes used by MongoDB."""

VALIDATORS = {
    "students": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["student_id", "name", "email", "department", "year", "cgpa"],
            "properties": {
                "student_id": {"bsonType": "string", "description": "must be a string"},
                "name": {"bsonType": "string", "minLength": 2},
                "email": {"bsonType": "string", "pattern": "^.+@.+\\..+$"},
                "phone": {"bsonType": "string"},
                "department": {"bsonType": "string"},
                "year": {"bsonType": "int", "minimum": 1, "maximum": 4},
                "cgpa": {"bsonType": ["double", "int", "decimal"], "minimum": 0, "maximum": 10},
                "skills": {"bsonType": "array", "items": {"bsonType": "string"}},
            },
        }
    },
    "companies": {
        "$jsonSchema": {
            "bsonType": "object", "required": ["company_id", "name", "industry", "location"],
            "properties": {
                "company_id": {"bsonType": "string"}, "name": {"bsonType": "string"},
                "industry": {"bsonType": "string"}, "location": {"bsonType": "string"},
                "website": {"bsonType": "string"},
            },
        }
    },
    "jobs": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["job_id", "company_id", "title", "package_lpa", "vacancies", "status"],
            "properties": {
                "job_id": {"bsonType": "string"}, "company_id": {"bsonType": "string"},
                "title": {"bsonType": "string"},
                "package_lpa": {"bsonType": ["double", "int", "decimal"], "minimum": 0},
                "location": {"bsonType": "string"}, "skills_required": {"bsonType": "array"},
                "vacancies": {"bsonType": "int", "minimum": 0},
                "status": {"enum": ["Open", "Closed"]},
            },
        }
    },
    "applications": {
        "$jsonSchema": {
            "bsonType": "object", "required": ["application_id", "student_id", "job_id", "application_date", "status"],
            "properties": {
                "application_id": {"bsonType": "string"}, "student_id": {"bsonType": "string"},
                "job_id": {"bsonType": "string"}, "application_date": {"bsonType": "date"},
                "status": {"enum": ["Applied", "Shortlisted", "Rejected", "Selected"]},
            },
        }
    },
    "interviews": {
        "$jsonSchema": {
            "bsonType": "object", "required": ["interview_id", "application_id", "round", "interview_date", "result"],
            "properties": {
                "interview_id": {"bsonType": "string"}, "application_id": {"bsonType": "string"},
                "round": {"bsonType": "string"}, "interview_date": {"bsonType": "date"},
                "result": {"enum": ["Scheduled", "Passed", "Failed"]},
            },
        }
    },
    "placements": {
        "$jsonSchema": {
            "bsonType": "object", "required": ["placement_id", "student_id", "company_id", "job_id", "package_lpa", "placement_date", "status"],
            "properties": {
                "placement_id": {"bsonType": "string"}, "student_id": {"bsonType": "string"},
                "company_id": {"bsonType": "string"}, "job_id": {"bsonType": "string"},
                "package_lpa": {"bsonType": ["double", "int", "decimal"], "minimum": 0},
                "placement_date": {"bsonType": "date"}, "status": {"enum": ["Placed"]},
            },
        }
    },
}

UNIQUE_INDEXES = {
    "students": ["student_id", "email"], "companies": ["company_id"], "jobs": ["job_id"],
    "applications": ["application_id"], "interviews": ["interview_id"], "placements": ["placement_id"],
}


def create_schema(db):
    """Create or update collections with strict validation and useful indexes."""
    existing = set(db.list_collection_names())
    for name, validator in VALIDATORS.items():
        options = {"validator": validator, "validationLevel": "strict", "validationAction": "error"}
        if name not in existing:
            db.create_collection(name, **options)
        else:
            db.command("collMod", name, **options)
        for field in UNIQUE_INDEXES[name]:
            db[name].create_index(field, unique=True)
    db.jobs.create_index([("status", 1), ("package_lpa", -1)])
    db.applications.create_index([("student_id", 1), ("job_id", 1)])
    db.placements.create_index("company_id")
