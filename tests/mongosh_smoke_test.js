// Run after queries/setup_database.js. It uses only the project database.
const placementDb = db.getSiblingDB("college_placement_db");

const expectedCounts = { students: 5, companies: 3, jobs: 4, applications: 5, interviews: 4, placements: 2 };
for (const [collection, expected] of Object.entries(expectedCounts)) {
  const actual = placementDb[collection].countDocuments();
  if (actual < expected) throw new Error(`${collection}: expected at least ${expected}, received ${actual}`);
}

const lookupRows = placementDb.applications.aggregate([
  { $lookup: { from: "students", localField: "student_id", foreignField: "student_id", as: "student" } },
  { $unwind: "$student" },
  { $project: { _id: 0, application_id: 1, "student.name": 1 } }
]).toArray();
if (lookupRows.length !== placementDb.applications.countDocuments()) throw new Error("$lookup did not enrich every application.");

let validationRejected = false;
try {
  placementDb.students.insertOne({ student_id: "INVALID_CGPA", name: "Invalid Test", email: "invalid@example.edu", department: "CSE", year: NumberInt(4), cgpa: 11 });
} catch (error) {
  validationRejected = true;
}
if (!validationRejected) throw new Error("Invalid CGPA was accepted; validation is not active.");

printjson({ result: "PASS", collections: expectedCounts, lookup_rows: lookupRows.length, validation: "invalid CGPA rejected" });
