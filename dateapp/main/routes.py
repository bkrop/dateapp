from flask import Blueprint, render_template
from dateapp.likes.forms import LikePerson, DislikePerson
from dateapp.models import User
from flask_login import login_required


main = Blueprint('main', __name__)

@main.route('/home', methods=['POST', 'GET'])
@main.route('/')
@login_required
def home():
    users = User.query.all()
    form = LikePerson()
    dislike_form = DislikePerson()
    return render_template('hometest.html', users=users, form=form, dislike_form=dislike_form)


