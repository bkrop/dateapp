from dateapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), default='')
    gender = db.Column(db.String(6), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    likes = db.relationship('Like', backref='liked_by', lazy='dynamic')
    dislikes = db.relationship('Dislike', backref='disliked_by', lazy='dynamic')

    def __repr__(self):
        return f'User({self.name}, {self.gender}, {self.age}, {self.image})'

class Like(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    like_to = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Like id: {self.id}, user id: {self.user_id}, like to: {self.like_to}, like from: {self.liked_by}"

class Dislike(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    dislike_to = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)