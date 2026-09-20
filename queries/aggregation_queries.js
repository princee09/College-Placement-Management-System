// Run in mongosh. The first line explicitly selects the project database.
const placementDb = db.getSiblingDB("college_placement_db");

// 1. Average job package
printjson(placementDb.jobs.aggregate([{ $group: { _id: null, average_package_lpa: { $avg: "$package_lpa" } } }]).toArray());

// 2. Highest offered package
printjson(placementDb.placements.aggregate([{ $group: { _id: null, highest_package_lpa: { $max: "$package_lpa" } } }]).toArray());

// 3. Application totals grouped by status
printjson(placementDb.applications.aggregate([{ $group: { _id: "$status", total: { $sum: 1 } } }, { $sort: { _id: 1 } }]).toArray());

// 4. Students grouped by department
printjson(placementDb.students.aggregate([{ $group: { _id: "$department", total_students: { $sum: 1 } } }, { $sort: { _id: 1 } }]).toArray());

// 5. Top-paying jobs
printjson(placementDb.jobs.aggregate([{ $sort: { package_lpa: -1 } }, { $limit: 5 }, { $project: { _id: 0, job_id: 1, title: 1, package_lpa: 1 } }]).toArray());

// 6. $lookup: applications enriched with student information
printjson(placementDb.applications.aggregate([
  { $lookup: { from: "students", localField: "student_id", foreignField: "student_id", as: "student" } },
  { $unwind: "$student" },
  { $project: { _id: 0, application_id: 1, status: 1, "student.name": 1, "student.department": 1, "student.cgpa": 1 } }
]).toArray());

// 7. Top hiring company with company name
printjson(placementDb.placements.aggregate([
  { $group: { _id: "$company_id", placements: { $sum: 1 } } }, { $sort: { placements: -1 } }, { $limit: 1 },
  { $lookup: { from: "companies", localField: "_id", foreignField: "company_id", as: "company" } },
  { $unwind: "$company" }, { $project: { _id: 0, company: "$company.name", placements: 1 } }
]).toArray());
