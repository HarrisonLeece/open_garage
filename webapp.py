#flask webapp https://exploreflask.com/en/latest/index.html
from flask import Flask, session, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

import sys
import re
from datetime import datetime
from datetime import timedelta #so that we can log last time user interacted with the server for session timeout

import random, string

#flask_wtf to help with form managemenmt and security https://exploreflask.com/en/latest/forms.html
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from util.validators import Unique
#Database relationships https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
from sqlalchemy.orm import declarative_base, relationship

#password encrpytion
from passlib.hash import sha256_crypt
#usage
#password = sha256_crypt.encrypt("user_password+salt")
#password_match = sha256_crypt.verify("user_password+salt", password)

#from models import user, tool, accessory

app = Flask(__name__, template_folder='templates')
app.config.update(TESTING=True, TEMPLATES_AUTO_RELOAD=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///corey_og.sqlite3'
#app.config['SQLACLCHEMY_BINDS'] = {"user_table": "sqlite:///user_table.sqlite3", "tool_table": "sqlite:///tool_table.sqlite3", "accessory_table": "sqlite:///accessory_table.sqlite3" }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['EXPLAIN_TEMPLATE_LOADING'] = False
app.secret_key = '1!df56dn;' #can be anything
#sessions data
app.permanent_session_lifetime = timedelta(hours=2)
#session.permanent=True #call this fater session dictionary is instantiated
db = SQLAlchemy(app)
db.app = app
app.config['database'] = db
with app.app_context():
    ######blueprint importation ##This has to occur after db setup or else runtime error (since the db will not be setup at import time)
    from blueprints.admin.admin_bp import admin_p
    from blueprints.admin.admin_test_bp import admin_test
    from blueprints.signin.signin_up import sign_in_bp
    from blueprints.garage.garage_bp import garage_bp
    ############## Blueprint registration
    app.register_blueprint(admin_p)
    app.register_blueprint(admin_test)

    app.register_blueprint(sign_in_bp)

    app.register_blueprint(garage_bp)
    ##############
################################


@app.before_first_request
def create_tables():
    db.create_all()

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

########### send user to sign up or to garage if token is fresh
@app.route("/", methods=['GET', 'POST'])
def home():
    valid_sign_in = True
    if (valid_sign_in):
        return redirect('/sign-in')
    else:
        return redirect('/garage')
###########


#tool-search
@app.route("/tool-search/", methods=["GET", "POST"])
def tool_search():
    pass

#advertise-service
@app.route("/advertise-service/", methods=["GET", "POST"])
def adv_service():
    pass

#search for local services
@app.route("/service-search/", methods=["GET", "POST"])
def service_search():
    pass

###########

########### helper/expansion features
#help using the site
@app.route("/help/", methods=['GET'])
def help():
    return render_template('help.html', title="Help")

#manage user settings
@app.route("/user_settings/", methods=['GET','POST'])
def user_settings():
    pass
#Neighborhood events or announcements
@app.route("/neighborhood/", methods=["GET", "POST"])
def neighborhood():
    return render_template('announcement.html', title="Neighborhood")

#projects
@app.route("/projects/", methods=["GET", "POST"])
def projects():
    return render_template('projects.html', title="Neighborhood Projects")

###########

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
