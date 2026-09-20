// Run in mongosh. The first line explicitly selects the project database.
const placementDb = db.getSiblingDB("college_placement_db");

// CREATE
placementDb.students.insertOne({
  student_id: "STU010", name: "Amit Kumar", email: "amit.kumar@example.edu",
  phone: "9876543220", department: "CSE", year: 4, cgpa: 8.2,
  skills: ["Python", "MongoDB"]
});

// READ: filter students by department, CGPA, and a skill
placementDb.students.find({ department: "CSE" });
placementDb.students.find({ cgpa: { $gte: 8.5 } });
placementDb.students.find({ skills: "Python" });
placementDb.jobs.find({ status: "Open" }).sort({ package_lpa: -1 });
placementDb.jobs.find({ package_lpa: { $gte: 8 } }).limit(5);
placementDb.applications.find({ status: "Shortlisted" });
placementDb.interviews.find({ result: "Passed" });
placementDb.placements.find({ company_id: "COMP001" });

// UPDATE
placementDb.students.updateOne({ student_id: "STU010" }, { $set: { cgpa: 8.5 } });
placementDb.applications.updateMany({ job_id: "JOB001", status: "Applied" }, { $set: { status: "Shortlisted" } });

// DELETE - run only after demonstrating create/read/update.
placementDb.students.deleteOne({ student_id: "STU010" });
