import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

print("URI loaded:", MONGO_URI)

client = MongoClient(
    os.getenv("MONGO_URI"),
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=10000
)

db = client["expense_tracker"]
expenses_collection = db["expenses"]
