from flask import render_template, flash, redirect, url_for
from dateapp import app, db, bcrypt
from dateapp.forms import RegistrationForm, LoginForm
from dateapp.models import User
from flask_login import login_user





@app.route('/register', methods=['POST', 'GET'])
def register():
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
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Incorrect email or password!')

    return render_template('login.html', form=form)


@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html', values=User.query.all())