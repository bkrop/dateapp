import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from dateapp import app, db, bcrypt, login_manager
from dateapp.forms import RegistrationForm, LoginForm, EditAccountForm, LikePerson, CreateMessageForm
from dateapp.models import User, Like, Match, Message
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, date

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        today = date.today()
        dob = form.date_of_birth.data
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        new_user = User(email=form.email.data, name=form.name.data,
                        age=age, gender=form.gender.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.email.data}!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))           
        else:
            flash('Incorrect email or password!')

    return render_template('login.html', form=form)


@app.route('/home', methods=['POST', 'GET'])
@app.route('/')
@login_required
def home():
    users = User.query.all()
    form = LikePerson()
    return render_template('hometest.html', users=users, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = EditAccountForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.description = form.description.data
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.description.data = current_user.description
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', form=form, image_file=image_file)

@app.route('/profile/like/<int:user_id>', methods=['POST'])
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
    return redirect(url_for('home'))

@app.route('/matches')
@login_required
def matches():
    matches = Match.query.all()
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('matches.html', matches=matches, image_file=image_file)

@app.route('/chat/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat(user_id):
    user = User.query.get_or_404(user_id)
    messages_by_user = current_user.messages_received.filter_by(by=user).all()
    messages_to_user = current_user.messages_sent.filter_by(to=user).all()
    messages = messages_by_user + messages_to_user
    form = CreateMessageForm()
    if form.validate_on_submit():
        new_message = Message(by=current_user, to=user, date_of_send=datetime.now(), content=form.content.data)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('chat', user_id=user.id))
    image_file = url_for('static', filename=f'profile_pics/{user.image_file}')
    return render_template('chat.html', form=form, messages=messages, user=user, image_file=image_file)
    
@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    image_file = url_for('static', filename=f'profile_pics/{user.image_file}')
    return render_template('profile.html', user=user, image_file=image_file)

