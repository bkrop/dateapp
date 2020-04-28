from flask import render_template, flash, redirect, url_for, request
from dateapp import app, db, bcrypt, login_manager
from dateapp.forms import RegistrationForm, LoginForm, EditAccountForm, LikePerson
from dateapp.models import User, Like, Match
from flask_login import login_user, current_user, logout_user, login_required





@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        new_user = User(email=form.email.data, name=form.name.data,
                        age=form.age.data, gender=form.gender.data, password=hashed_password)
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
def home():
    users = User.query.all()
    form = LikePerson()
    return render_template('hometest.html', users=users, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = EditAccountForm()
    if form.validate_on_submit():
        current_user.description = form.description.data
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.description.data = current_user.description
    return render_template('account.html', form=form)

@app.route('/profile/like/<int:user_id>', methods=['POST'])
@login_required
def like_profile(user_id):
    user = User.query.get_or_404(user_id)
    new_like = Like(liked_by=current_user, like_to=user)
    db.session.add(new_like)
    likes = Like.query.all()
    for like in likes:
        if new_like.like_to == like.liked_by and like.like_to == current_user:
            new_match = Match(user1 = current_user, user2 = user)
            db.session.add(new_match)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/matches')
@login_required
def matches():
    matches = Match.query.all()
    return render_template('matches.html', matches=matches)

