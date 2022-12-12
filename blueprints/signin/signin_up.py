from flask import Blueprint, render_template, abort, url_for, request, flash, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from util.validators import Unique
from datetime import datetime
from models import user, tool, accessory


app = current_app
with app.app_context():
    db = current_app.config['database']
    sign_in_bp = Blueprint('sign-in', __name__, template_folder='templates/signin', static_folder='static')

################################################################################
#######WTForms
class EmailPasswordForm(FlaskForm):
    #pretty crazy, but the variable name has to match the name of the field in html
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Unique(user,user.user_name, message='There is already an accoutn using that username')])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Unique(user,user.email, message='There is already an accoutn using that email')])

#######

###############
def create_new_user(username, password, vpass, email):
    #verify matching passwords
    if (password != vpass):
        return False
    #verify unique username in Database
    if (username != "Harrison"):
        return False
    #verify unique email
    if (email != "harryleecemail@gmail.com"):
        return False
    #after verification, do work to commit to db
    new_user = user(username, password, email)
    db.session.add(new_user)
    db.session.commit()

    return True

def verify_login_credentials(user_or_email, password_in):
    type = "user"
    server_pass = ""
    salt = ""
    if (user_or_email.find("@") != -1):
        type = "email"
    if (type == "user"):
        #see if user name exists in the user_table.users
        print(user_or_email)
        user_row = db.session.query(user).filter(user.user_name==user_or_email).all()
        #print(db.session.query(user).filter(user==user_or_email))
        print(user_row[0].user_name)
        if (user_row):
            #get password hash and salt
            verified = user_row[0].verify_password_hash(password_in)
            print(verified)
            return verified
    #this else occurse if type == "email"
    else:
        #see if email exists in the user_table.email
        user_row = db.session.query(user).filter(user.email==user_or_email).all()
        if (user_row):
            #get password hash and salt
            verified = user_row[0].verify_password_hash(password_in)
            return verified
    #This is false only if username or email is not in the database
    return False

###############


########### reconditon .txt file list to raw text
#in list is the list returned by .readlines() containing lists of strings with \n as break
def parse_announcement(in_list):
    string_annc = ''
    for str in in_list:
        if (str == '\n'):
            string_annc = string_annc + ' <br> '
        elif (str[-2:-1] == '\n'):
            string_annc = string_annc + str[0:-2] + ' <br> '
        else:
            string_annc = string_annc + str
    return string_annc
#does not currently space lines correctly.

########### Sign in and sign up
@sign_in_bp.route("/sign-in/", methods=["GET", "POST"])
def sign_in():
    announce_txt = "Standin announcement"
    sign_in_form = EmailPasswordForm()
    with open('./static/announcements.txt', 'r') as annc:
        announce_txt = annc.readlines() #announce_txt is now a list, as per readlines()
    announce_txt = parse_announcement(announce_txt) #announce_txt is now a string containing html tags

    if (not sign_in_form.validate_on_submit()):
        flash(sign_in_form.errors)
    if request.method == "POST" and sign_in_form.validate_on_submit():

        user = request.form["username"]
        passw = request.form["password"]
        #get all the login information
        #get announcement information
        login_verified = verify_login_credentials(user,passw)

        #if a correct username password combination is received, redirect to garage
        if(login_verified):
            print("User logged in!")
            #if sign in is successful, redirect user to garage with a populated session
            return redirect('/garage')
        else:
            flash(sign_in_form.errors)
            #if signup fails, send the user back to the login page to retry
            return render_template('login_main.html', title="Login POST", announcement=announce_txt, form=sign_in_form)

    else:
        return render_template('login_main.html', title="Login GET", announcement=announce_txt, form=sign_in_form)

#Sign up for open garage and create a new user
@sign_in_bp.route("/sign-up/", methods=["GET", "POST"])
def sign_up():
    announce_txt = "Standin announcement"
    sign_up_form = SignUpForm()
    with open('./static/announcements.txt', 'r') as annc:
        announce_txt = annc.readlines() #announce_txt is now a list, as per readlines()
    announce_txt = parse_announcement(announce_txt) #announce_txt is now a string containing html tags
    if (not sign_up_form.validate_on_submit()):
        flash(sign_up_form.errors)
    if request.method == "POST" and sign_up_form.validate_on_submit():

        user = request.form["username"]
        passw = request.form["password"] #this has to match
        vpassw = request.form["vpassword"] #this
        email = request.form["email"]
        #get all the login information
        #get announcement information
        success = create_new_user(user,passw,vpassw,email)
        #if a correct username password combination is received, redirect to garage
        if(success):
            #if sign up is successful redirect to login and force user to login
            return redirect('/sign-in/')
        else:
            flash(sign_up_form.errors)
            #if sign up is invalid or unsuccessful for whatever reason,
            return render_template('sign-up_main.html', title="Login POST", announcement=announce_txt, form=sign_up_form)

    else:
        flash(sign_up_form.errors)
        return render_template('sign-up_main.html', title="Login GET", announcement=announce_txt, form=sign_up_form)

###########
