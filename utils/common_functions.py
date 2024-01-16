from utils.db_utils import db
from flask import request, redirect, make_response
from utils.constants import ROLE, SESSION_COOKIE, USERNAME_COOKIE
from utils.db_utils import get_user_session_key, update_user_session_key
import uuid


# find if the user has no role
def is_first_time_register(username):
    user_data = db.user_data.find_one({'username': username})
    if ROLE in user_data.keys():
        return False
    return True

# set the user role
def set_user_role(username, role):
    db_response = db.user_data.update_one({'username': username}, {'$set': {'role': role}})
    return db_response.matched_count == 1

# set a new session key and redirect to dashboard 
def set_user_session_key_and_redirect_to_dashboard():
    user_session_key = generate_session_key()
    if update_user_session_key(username=request.form['username'], session_key=user_session_key):
        response = make_response(redirect('/dashboard'))
        response.set_cookie(USERNAME_COOKIE, request.form['username'])
        response.set_cookie(SESSION_COOKIE, user_session_key)
        return response
    return False

# check if the user is logged in and the session key matches the current session
def is_user_valid(request):
    if request.cookies.get(USERNAME_COOKIE) != None and request.cookies.get(SESSION_COOKIE) != None:
        return get_user_session_key(username=request.cookies.get(USERNAME_COOKIE)) == request.cookies.get(SESSION_COOKIE)
    return False

# function to generate_session_key
def generate_session_key():
    return uuid.uuid4().hex
