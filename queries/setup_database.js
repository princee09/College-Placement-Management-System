// Optional non-Python setup path for mongosh/Compass demonstrations.
// The Python setup_database.py remains the primary application setup command.
const dbName = "college_placement_db";
db = db.getSiblingDB(dbName);

const schemas = {
  students: { required: ["student_id", "name", "email", "department", "year", "cgpa"], properties: { student_id: { bsonType: "string" }, name: { bsonType: "string" }, email: { bsonType: "string", pattern: "^.+@.+\\..+$" }, department: { bsonType: "string" }, year: { bsonType: "int", minimum: 1, maximum: 4 }, cgpa: { bsonType: ["double", "int", "decimal"], minimum: 0, maximum: 10 }, skills: { bsonType: "array" } } },
  companies: { required: ["company_id", "name", "industry", "location"], properties: { company_id: { bsonType: "string" }, name: { bsonType: "string" }, industry: { bsonType: "string" }, location: { bsonType: "string" } } },
  jobs: { required: ["job_id", "company_id", "title", "package_lpa", "vacancies", "status"], properties: { job_id: { bsonType: "string" }, company_id: { bsonType: "string" }, title: { bsonType: "string" }, package_lpa: { bsonType: ["double", "int", "decimal"], minimum: 0 }, vacancies: { bsonType: "int", minimum: 0 }, status: { enum: ["Open", "Closed"] } } },
  applications: { required: ["application_id", "student_id", "job_id", "application_date", "status"], properties: { application_id: { bsonType: "string" }, student_id: { bsonType: "string" }, job_id: { bsonType: "string" }, application_date: { bsonType: "date" }, status: { enum: ["Applied", "Shortlisted", "Rejected", "Selected"] } } },
  interviews: { required: ["interview_id", "application_id", "round", "interview_date", "result"], properties: { interview_id: { bsonType: "string" }, application_id: { bsonType: "string" }, round: { bsonType: "string" }, interview_date: { bsonType: "date" }, result: { enum: ["Scheduled", "Passed", "Failed"] } } },
  placements: { required: ["placement_id", "student_id", "company_id", "job_id", "package_lpa", "placement_date", "status"], properties: { placement_id: { bsonType: "string" }, student_id: { bsonType: "string" }, company_id: { bsonType: "string" }, job_id: { bsonType: "string" }, package_lpa: { bsonType: ["double", "int", "decimal"], minimum: 0 }, placement_date: { bsonType: "date" }, status: { enum: ["Placed"] } } }
};

for (const [collection, schema] of Object.entries(schemas)) {
  const options = { validator: { $jsonSchema: { bsonType: "object", ...schema } }, validationLevel: "strict", validationAction: "error" };
  if (!db.getCollectionNames().includes(collection)) db.createCollection(collection, options);
  else db.runCommand({ collMod: collection, ...options });
}

const data = {
  students: [
    { student_id: "STU001", name: "Rahul Sharma", email: "rahul.sharma@example.edu", phone: "9876543210", department: "CSE", year: NumberInt(4), cgpa: 8.45, skills: ["Python", "MongoDB", "Machine Learning"] },
    { student_id: "STU002", name: "Ananya Iyer", email: "ananya.iyer@example.edu", phone: "9876543211", department: "ISE", year: NumberInt(4), cgpa: 9.10, skills: ["Java", "SQL", "React"] },
    { student_id: "STU003", name: "Vikram Singh", email: "vikram.singh@example.edu", phone: "9876543212", department: "CSE", year: NumberInt(4), cgpa: 7.90, skills: ["Python", "Git", "Docker"] },
    { student_id: "STU004", name: "Meera Nair", email: "meera.nair@example.edu", phone: "9876543213", department: "ECE", year: NumberInt(4), cgpa: 8.20, skills: ["C++", "IoT", "Python"] },
    { student_id: "STU005", name: "Arjun Das", email: "arjun.das@example.edu", phone: "9876543214", department: "CSE", year: NumberInt(4), cgpa: 8.75, skills: ["Python", "MongoDB", "Git"] }
  ],
  companies: [{ company_id: "COMP001", name: "TechNova Solutions", industry: "Information Technology", location: "Bengaluru", website: "https://technova.example" }, { company_id: "COMP002", name: "DataSphere Analytics", industry: "Analytics", location: "Hyderabad", website: "https://datasphere.example" }, { company_id: "COMP003", name: "CloudAxis Systems", industry: "Cloud Computing", location: "Pune", website: "https://cloudaxis.example" }],
  jobs: [{ job_id: "JOB001", company_id: "COMP001", title: "Software Developer", package_lpa: 8.5, location: "Bengaluru", skills_required: ["Python", "MongoDB", "Git"], vacancies: NumberInt(10), status: "Open" }, { job_id: "JOB002", company_id: "COMP002", title: "Data Analyst", package_lpa: 7.2, location: "Hyderabad", skills_required: ["Python", "SQL"], vacancies: NumberInt(5), status: "Open" }, { job_id: "JOB003", company_id: "COMP003", title: "Cloud Engineer", package_lpa: 10, location: "Pune", skills_required: ["Docker", "Python", "AWS"], vacancies: NumberInt(4), status: "Open" }, { job_id: "JOB004", company_id: "COMP001", title: "Frontend Developer", package_lpa: 6.8, location: "Bengaluru", skills_required: ["React", "JavaScript"], vacancies: NumberInt(3), status: "Closed" }],
  applications: [{ application_id: "APP001", student_id: "STU001", job_id: "JOB001", application_date: ISODate("2026-09-05"), status: "Selected" }, { application_id: "APP002", student_id: "STU002", job_id: "JOB002", application_date: ISODate("2026-09-06"), status: "Shortlisted" }, { application_id: "APP003", student_id: "STU003", job_id: "JOB003", application_date: ISODate("2026-09-07"), status: "Applied" }, { application_id: "APP004", student_id: "STU004", job_id: "JOB001", application_date: ISODate("2026-09-08"), status: "Rejected" }, { application_id: "APP005", student_id: "STU005", job_id: "JOB001", application_date: ISODate("2026-09-09"), status: "Selected" }],
  interviews: [{ interview_id: "INT001", application_id: "APP001", round: "Technical", interview_date: ISODate("2026-09-12"), result: "Passed" }, { interview_id: "INT002", application_id: "APP002", round: "Technical", interview_date: ISODate("2026-09-13"), result: "Scheduled" }, { interview_id: "INT003", application_id: "APP004", round: "HR", interview_date: ISODate("2026-09-14"), result: "Failed" }, { interview_id: "INT004", application_id: "APP005", round: "HR", interview_date: ISODate("2026-09-15"), result: "Passed" }],
  placements: [{ placement_id: "PLC001", student_id: "STU001", company_id: "COMP001", job_id: "JOB001", package_lpa: 8.5, placement_date: ISODate("2026-09-20"), status: "Placed" }, { placement_id: "PLC002", student_id: "STU005", company_id: "COMP001", job_id: "JOB001", package_lpa: 8.5, placement_date: ISODate("2026-09-21"), status: "Placed" }]
};
const idFields = { students: "student_id", companies: "company_id", jobs: "job_id", applications: "application_id", interviews: "interview_id", placements: "placement_id" };
for (const [collection, documents] of Object.entries(data)) for (const document of documents) db[collection].replaceOne({ [idFields[collection]]: document[idFields[collection]] }, document, { upsert: true });
db.students.createIndex({ student_id: 1 }, { unique: true }); db.students.createIndex({ email: 1 }, { unique: true });
for (const [collection, field] of Object.entries({ companies: "company_id", jobs: "job_id", applications: "application_id", interviews: "interview_id", placements: "placement_id" })) db[collection].createIndex({ [field]: 1 }, { unique: true });
print(`Setup complete: ${dbName}. Collections: ${db.getCollectionNames().sort().join(", ")}`);
