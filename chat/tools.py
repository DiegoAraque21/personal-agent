from dotenv import load_dotenv
import os
from pymongo import MongoClient
import certifi
load_dotenv(override=True)

class MongoDB:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"), tls=True, tlsCAFile=certifi.where())
        self.db = self.client[os.getenv("MONGO_DB_CLIENT")]
        self.collection = self.db[os.getenv("MONGO_DB_COLLECTION")]

    def record_user_details(self, email: str, name: str = "", notes: str = "") -> dict:
        """
        Records the user's details in the database.
        :param email: the email of the user
        :param name: the name of the user
        :param notes: the notes of the user
        :return: a dictionary containing the status and message
        """
        # make it use the client
        
        self.collection.insert_one({"email": email, "name": name, "notes": notes})
        return {"status": "success", "message": "User details recorded successfully"}
        
    def get_user_details(self, email: str) -> dict:
        """
        Gets the user's details from the database.
        :param email: the email of the user
        :return: a dictionary containing the user's details
        """
        return self.collection.find_one({"email": email})

mongo_db = MongoDB()

def _record_user_details(email: str, name: str = "", notes: str = "") -> dict:
    mongo_db.record_user_details(email, name, notes)
    return {"status": "success", "message": "User details recorded successfully"}

def _get_user_details(email: str) -> dict:
    return mongo_db.get_user_details(email)