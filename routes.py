from flask import render_template, request, redirect, make_response, Blueprint
from utils.common_functions import is_first_time_register, is_user_valid, set_user_role, set_user_session_key_and_redirect_to_dashboard
from utils.constants import DONOR, LOGIN_ERROR_MSG, RECEIVER, REGISTRATION_FAILURE_MESSAGE, REGISTRATION_NOT_APPLICABLE_MESSAGE, REGISTRATION_SUCCESS_MESSAGE, SESSION_COOKIE, SHOW_NOTIFICATION, TEST_IMAGES_PATH, USERNAME_COOKIE
from utils.db_utils import add_new_user
from utils.chatbot_utils import chatbot_response
from utils.cox_utils import predict_wait_time
from utils.dffn_utils import predict_kidney_diesease
from utils.db_utils import add_new_user, update_user_session_key, validate_user
import os


routes = Blueprint('routes', __name__)


# Register as Donor
@routes.route('/register', methods=['POST'])
def register_user_as_donor():
    if is_user_valid(request=request) and is_first_time_register(request.cookies.get(USERNAME_COOKIE)):
        if set_user_role(username=request.cookies.get(USERNAME_COOKIE), role=list(request.form.keys())[0]):
            return redirect(f'/dashboard?{SHOW_NOTIFICATION}=success')
        else:
            return redirect(f'/dashboard?{SHOW_NOTIFICATION}=failure')
    else:
        return redirect(f'/dashboard?{SHOW_NOTIFICATION}=notApplicable')


# User Sign Up
@routes.route('/createNewUser', methods=['POST'])
def create_new_user():
    if add_new_user(user_information=request.form):
        # user_session_key = get_user_session_key(username=request.form['username'])
        return set_user_session_key_and_redirect_to_dashboard()
    else:
        return render_template('login.html')    

# Login route
@routes.route('/login', methods=['GET'])
def login():
    if is_user_valid(request=request):
        return redirect('/dashboard')
    return render_template('login.html')

# login route 
@routes.route('/login', methods=['POST'])
def login_user():
    if validate_user(user_information=request.form):
        return set_user_session_key_and_redirect_to_dashboard()
    
    return render_template('login.html', login_error_msg = LOGIN_ERROR_MSG) 

# Dashboard route
@routes.route('/dashboard')
def user_dashboard():
    show_notification, notification_msg, first_time = False, '', is_first_time_register(request.cookies.get(USERNAME_COOKIE))
    if is_user_valid(request=request):
        if request.args.get(SHOW_NOTIFICATION) == 'success':
            show_notification, notification_msg = True, REGISTRATION_SUCCESS_MESSAGE
        elif request.args.get(SHOW_NOTIFICATION) == 'failure':
            show_notification, notification_msg = True, REGISTRATION_FAILURE_MESSAGE
        elif request.args.get(SHOW_NOTIFICATION) == 'notApplicable':
            show_notification, notification_msg = True, REGISTRATION_NOT_APPLICABLE_MESSAGE 
        return render_template('index.html', first_time=first_time, show_notification=show_notification, notification_msg=notification_msg)
    else:
        return redirect('/login')
    
# Modules route
@routes.route('/modules')
def modules():
    if is_user_valid(request=request):
        return render_template('modules.html')
    else:
        return redirect('/login')

# Chatbot route
@routes.route('/chatbot', methods=['POST'])
def get_chatbot_response():
    return chatbot_response(request.form['user_response'])

# DFFN route
@routes.route('/dffn', methods=['POST'])
def get_dffn_response():
    file_path = ""
    if 'file' in request.files:
        file = request.files['file']
        if file:
            file_path = os.path.join(TEST_IMAGES_PATH, file.filename)
            file.save(file_path)
    return predict_kidney_diesease(file_path)

# COX route
@routes.route('/cox', methods=['POST'])
def get_wait_time():
    return predict_wait_time(request.form)

# Log out route
@routes.route('/logout')
def logout_user():
    response = make_response(redirect('/login'))
    update_user_session_key(username=request.cookies.get(USERNAME_COOKIE), session_key='')
    response.set_cookie(USERNAME_COOKIE, '', expires=0)
    response.set_cookie(SESSION_COOKIE, '', expires=0)
    return response