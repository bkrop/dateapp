from flask import render_template, flash, redirect, url_for, request
from dateapp import app, db, bcrypt
from dateapp.forms import RegistrationForm, LoginForm, EditAccountForm, LikePerson
from dateapp.models import Like, User, Dislike
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
def like_profile(user_id):
    user = User.query.get_or_404(user_id)
    like = Like(like_to=user.id, liked_by=current_user)
    db.session.add(like)
    db.session.commit()
    flash(f'Like has been given to {user} from {current_user}. {type(current_user.likes)}')
    return redirect(url_for('home'))

@app.route('/profile/dislike/<int:user_id>', methods=['POST'])
def dislike_profile(user_id):
    user = User.query.get_or_404(user_id)
    dislike = Dislike(dislike_to=user.id, disliked_by=current_user)
    db.session.add(dislike)
    db.session.commit()
    return redirect(url_for('home'))