# College Placement Management System

An individual CA-2 MongoDB project implemented with Python and PyMongo. It manages students, companies, job openings, applications, interviews, and final placement offers.

## What is implemented

- Six related MongoDB collections using document references where entities have independent lifecycles.
- Strict MongoDB `$jsonSchema` validation and unique indexes.
- Realistic, repeatable sample data.
- Create, read, update, and delete operations through the Python menu and `mongosh` examples.
- Aggregations for average/highest package, applications by status, department totals, top jobs, hiring company, and `$lookup` joins.
- A live placement report: every number is calculated from MongoDB data.

## Prerequisites

- Python 3.10 or later
- MongoDB Community Server running locally, or a MongoDB Atlas URI

## Run in order

1. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env`. Keep the local URI or set your Atlas URI.

4. Start MongoDB, then create collections, validators, indexes, and sample data:

   ```powershell
   python setup_database.py
   ```

5. Start the polished web dashboard (recommended):

   ```powershell
   python web_app.py
   ```

   Then open `http://127.0.0.1:5000` in your browser.

6. Or start the menu-driven terminal application:

   ```powershell
   python main.py
   ```

7. For the MongoDB-shell evidence required in the report, run the scripts in `queries/` using mongosh.

## Demonstration order

1. Run `setup_database.py` and show the six collections in MongoDB Compass/mongosh.
2. Show a valid new student through option 1.
3. Try an invalid CGPA such as `11` to demonstrate validation rejection.
4. Use options 2, 3, and 4 for read, update, and controlled deletion.
5. Add a company/job, create an application, and schedule an interview.
6. Run menu option 14 for required aggregation pipelines and `$lookup` output.
7. Run option 13 and capture the final report output.

## Project layout

```text
database/       connection, validators, and sample data
operations/     aggregation-based placement reporting
queries/        directly runnable mongosh CRUD and aggregation scripts
main.py         interactive PyMongo application
setup_database.py  schema/index/sample-data setup
```

## Design rationale

Placement entities are separate collections because students, companies, jobs, applications, interviews, and placements each change independently. IDs are referenced between collections so updates do not duplicate company/student information. Skills are embedded arrays because they naturally belong to one student or one job and are queried together with that parent document.
