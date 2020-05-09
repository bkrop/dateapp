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
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    likes_given = db.relationship('Like', backref='by', lazy='dynamic', foreign_keys='Like.user_id')
    likes_received = db.relationship('Like', backref='to', lazy='dynamic', foreign_keys='Like.liked_user_id')
    dislikes_given = db.relationship('Dislike', backref='by', lazy='dynamic', foreign_keys='Dislike.user_id')
    dislikes_received = db.relationship('Dislike', backref='to', lazy='dynamic', foreign_keys='Dislike.disliked_user_id')
    matches = db.relationship('Match', backref='user1', lazy='dynamic', foreign_keys='Match.user1_id')
    matched_with = db.relationship('Match', backref='user2', lazy='dynamic', foreign_keys='Match.user2_id')
    messages_sent = db.relationship('Message', backref='by', lazy='dynamic', foreign_keys='Message.sender_id')
    messages_received = db.relationship('Message', backref='to', lazy='dynamic', foreign_keys='Message.receiver_id')
    
    def __repr__(self):
        return f'User({self.name}, {self.gender}, {self.age}, {self.image_file})'

class Like(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    liked_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Dislike(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    disliked_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Match(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Message(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    date_of_send = db.Column(db.DateTime, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
