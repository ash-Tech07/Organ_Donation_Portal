from flask_pymongo import PyMongo
from hashlib import sha512
from app import app
from dotenv import load_dotenv
import os
import uuid


load_dotenv()
mongodb_client = PyMongo(app, uri=os.getenv('DATABASE_URI'))
db = mongodb_client.db


def add_new_user(user_information):
    response = False
    user_information = dict(user_information)
    user_information['password'] = str(sha512(user_information['password'].encode()).hexdigest())
    user_information['session_key'] = uuid.uuid4().hex
    if db is not None:
        db.user_data.insert_one(dict(user_information))
        response = True
    else:
        print("Cannot connect to database!")
    return response

def validate_user(user_information):
    isUserValid = False
    if db is not None:
        user_data = db.user_data.find_one({ 'username': user_information['username'] })
        if user_data and str(sha512(user_information['password'].encode()).hexdigest()) == user_data['password']:
            isUserValid = True
    else:
        print("Cannot connect to database!")
    return isUserValid

def update_user_session_key(username, session_key):
    if db is not None:
        response = db.user_data.update_one({'username': username}, {'$set': {'session_key': session_key}})
        return response.matched_count == 1
    return False

def get_user_session_key(username):
    if db is not None:
        session_key = db.user_data.find_one({'username': username})['session_key']
        return session_key
    return False
