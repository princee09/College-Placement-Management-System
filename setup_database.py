"""Create validated collections, indexes, and demonstration data."""
from database.connection import get_database
from database.sample_data import seed_database
from database.validation import create_schema

if __name__ == "__main__":
    db = get_database()
    create_schema(db)
    seed_database(db)
    print(f"Setup complete: {db.name}")
    print("Collections:", ", ".join(sorted(db.list_collection_names())))
