"""MongoDB connection utilities."""
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()


def get_database():
    """Return a verified database connection or raise a clear error."""
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    database_name = os.getenv("MONGODB_DB", "college_placement_db")
    client = MongoClient(uri, serverSelectionTimeoutMS=4000)
    try:
        client.admin.command("ping")
    except ServerSelectionTimeoutError as error:
        raise RuntimeError(
            "MongoDB is not reachable. Start MongoDB, then check MONGODB_URI in .env."
        ) from error
    return client[database_name]
