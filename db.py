import os
import certifi


from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI"),
    tls=True,
    tlsCAFile=certifi.where()
)

db = client["expense_tracker"]

expenses_collection = db["expenses"]