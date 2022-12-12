from flask import Blueprint, render_template, abort, url_for, request, flash, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from util.validators import Unique
from datetime import datetime


app = current_app
with app.app_context():
    db = current_app.config['database']
    admin_p = Blueprint('admin', __name__, template_folder='templates/admin', static_folder='static')

class AdminForm(FlaskForm):
    #pretty crazy, but the variable name has to match the name of the field in html
    target_username = StringField('target_user', validators=[DataRequired()])

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

#############################################

#drops all tables
#def clear_data(session):
#    meta = db.metadata
#    for table in reversed(meta.sorted_tables):
#        print('Clear table %s' % table)
#        session.execute(table.delete())
#    session.commit()


@admin_p.route('/admin/', methods=["GET", "POST"])
def admin_prod():
    log_txt = "LOG NOT LOADED"
    with open('./static/cory_garage.log', 'r') as lg:
        log_txt = lg.readlines() #announce_txt is now a list, as per readlines()
    log_txt = parse_log(log_txt)
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
        elif (request.form['submit_post'] == 'erase_database'):
            reverse_suspension(request.form['target_username'])

        return render_template('admin/admin_production.html', title = "admin", log=log_txt, form = admin_form)
    else:
        return render_template('admin/admin_production.html', title = "admin", log=log_txt, form = admin_form)
