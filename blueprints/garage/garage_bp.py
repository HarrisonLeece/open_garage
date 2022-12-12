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
    garage_bp = Blueprint('garage', __name__, template_folder='templates/garage', static_folder='static')


#this should check for valid session login token
@garage_bp.route("/garage/", methods=["GET", "POST"])
def garage_page():
    return render_template('manage_garage.html', title="Manage Garage", username="hardcoded_username")
