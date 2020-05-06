from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_required, login_user, logout_user
from dateapp.models import User
from dateapp.users.forms import RegistrationForm, LoginForm, EditAccountForm
from dateapp import db, bcrypt
from datetime import date
from dateapp.users.utils import save_picture

users = Blueprint('users', __name__)

@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))           
        else:
            flash('Incorrect email or password!')

    return render_template('login.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['POST', 'GET'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.description.data = current_user.description
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', form=form, image_file=image_file)

@users.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    image_file = url_for('static', filename=f'profile_pics/{user.image_file}')
    return render_template('profile.html', user=user, image_file=image_file)