from flask import Blueprint, render_template, abort, url_for, request, current_app, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from util.validators import Unique
from datetime import datetime

app = current_app
with app.app_context():
    db = current_app.config['database']
    admin_test = Blueprint('admin_test', __name__, template_folder="templates", static_folder='static')

class AdminForm(FlaskForm):
    target_user = StringField('target_username')

#in list is the list returned by .readlines() containing lists of strings with \n as break
def parse_log(in_list):
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

#############################################Admin functions
#reset password
def reset_password(usr_in):
    now = datetime.now()
    #write action to log
    with open('./static/cory_garage.log', 'a') as lg:
        str = now.strftime("%Y/%m/%d") + " resetting " + usr_in + "'s password" + "\n"
        lg.write(str)
    #actually reset password in the database
    #send email to user?
#remove user
def remove_user(usr_in):
    now = datetime.now()
    #write action to log
    with open('./static/cory_garage.log', 'a') as lg:
        str = now.strftime("%Y/%m/%d") + " removing " + usr_in + " and asscociated items" + "\n"
        lg.write(str)
    #remove the user from the database
#suspend_user
def sus_user(usr_in):
    now = datetime.now()
    #write action to log
    with open('./static/cory_garage.log', 'a') as lg:
        str = now.strftime("%Y/%m/%d") + " suspending " + usr_in + " indefinitely " + "\n"
        lg.write(str)
    #actully suspend user and hide their tools
#add point
def add_point(usr_in):
    now = datetime.now()
    #write action to log
    with open('./static/cory_garage.log', 'a') as lg:
        str = now.strftime("%Y/%m/%d") + " adding 1 point to " + usr_in + "\n"
        lg.write(str)
    #add a fun point
#reverse_suspension
def reverse_suspension(usr_in):
    now = datetime.now()
    with open('./static/cory_garage.log', 'a') as lg:
        str =  now.strftime("%Y/%m/%d") + " reversing suspension for " + usr_in + "\n"
        lg.write(str)
    #actually change status of user in Database
#####testing only
def erase_database():
    now = datetime.now()
    #if clear_data fails this will keep a log
    with open('./static/cory_garage.log', 'a') as lg:
        str =  now.strftime("%Y/%m/%d") + " Dropping all tables in database "  + "\n"
        lg.write(str)
    clear_data()
    with open('./static/cory_garage.log', 'w') as lg:
        str =  now.strftime("%Y/%m/%d") + " All tables in database dropped "  + "\n"
        lg.write(str)

#drops all tables
def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()
#############################################

@admin_test.route('/admin-test/', methods=["GET", "POST"])
def admin_test_page():
    log_txt = "LOG NOT LOADED"
    admin_form = AdminForm()
    #only flash if there is an error
    if (not admin_form.validate_on_submit()):
        flash(admin_form.errors)

    if request.method == "POST" and admin_form.validate_on_submit():
        if (request.form['submit_post'] == 'reset_password'):
            reset_password(request.form['target_username'])
        elif (request.form['submit_post'] == 'remove_user'):
            remove_user(request.form['target_username'])
        elif (request.form['submit_post'] == 'suspend_user'):
            sus_user(request.form['target_username'])
        elif (request.form['submit_post'] == 'add_point'):
            add_point(request.form['target_username'])
        elif (request.form['submit_post'] == 'reverse_suspension'):
            reverse_suspension(request.form['target_username'])
        elif (request.form['submit_post'] == 'erase_database' and request.form['target_username'] == "admin"):
            erase_database()

    if request.method == "POST" and admin_form.validate_on_submit():
        #if post, refresh the log with the newest changes to the database
        with open('./static/cory_garage.log', 'r') as lg:
            log_txt = lg.readlines() #announce_txt is now a list, as per readlines()
        log_txt = parse_log(log_txt)
        return render_template('admin/admin_test.html', title = "admin_test", log=log_txt, form = admin_form)
    else:
        #get log
        with open('./static/cory_garage.log', 'r') as lg:
            log_txt = lg.readlines() #announce_txt is now a list, as per readlines()
        log_txt = parse_log(log_txt)
        return render_template('admin/admin_test.html', title = "admin_test", log=log_txt, form = admin_form)
