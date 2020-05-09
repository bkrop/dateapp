from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user
from dateapp.models import User, Like, Match, Dislike
from dateapp import db, login_manager

likes = Blueprint('likes', __name__)

@likes.route('/profile/like/<int:user_id>', methods=['POST'])
@login_required
def like_profile(user_id):
    user = User.query.get_or_404(user_id)
    new_like = Like(by=current_user, to=user)
    db.session.add(new_like)
    likes = Like.query.all()
    for like in likes:
        if new_like.to == like.by and like.to == current_user:
            new_match = Match(user1 = current_user, user2 = user)
            db.session.add(new_match)
    db.session.commit()
    return redirect(url_for('main.home'))

@likes.route('/profile/dislike/<int:user_id>', methods=['POST'])
@login_required
def dislike_profile(user_id):
    user = User.query.get_or_404(user_id)
    new_dislike = Dislike(to=user, by=current_user)
    db.session.add(new_dislike)
    db.session.commit()
    return redirect(url_for('main.home'))