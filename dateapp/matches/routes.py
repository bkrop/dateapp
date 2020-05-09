from flask import Blueprint, url_for, render_template
from flask_login import login_required, current_user
from dateapp.models import Match

matches = Blueprint('matches', __name__)

@matches.route('/your_matches')
@login_required
def your_matches():
    matches = current_user.matches.all() + current_user.matched_with.all()
    return render_template('your_matches.html', matches=matches)