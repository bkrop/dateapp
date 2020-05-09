from flask import Blueprint, redirect, render_template, url_for, abort
from flask_login import login_required, current_user
from dateapp.models import User, Message, Match
from dateapp.messagess.forms import CreateMessageForm
from datetime import datetime
from dateapp import db

messagess = Blueprint('messagess', __name__)

@messagess.route('/chat/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat(user_id):
    user = User.query.get_or_404(user_id)
    matches = current_user.matches.filter_by(user1=user).all() + current_user.matches.filter_by(user2=user).all() + current_user.matched_with.filter_by(user2=user).all() + current_user.matched_with.filter_by(user1=user).all()
    if user not in matches:
        abort(404)
    messages_by_user = current_user.messages_received.filter_by(by=user).all()
    messages_to_user = current_user.messages_sent.filter_by(to=user).all()
    messages = messages_by_user + messages_to_user
    form = CreateMessageForm()
    if form.validate_on_submit():
        new_message = Message(by=current_user, to=user, date_of_send=datetime.now(), content=form.content.data)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('messagess.chat', user_id=user.id))
    image_file = url_for('static', filename=f'profile_pics/{user.image_file}')
    return render_template('chat.html', form=form, messages=messages, user=user, image_file=image_file)