from dateapp.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, equal_to, ValidationError


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=100)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    age = IntegerField('Age', validators=[DataRequired()])
    description = StringField('Description', validators=[Length(max=200)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=60)])
    confirm_password = PasswordField('Confirm password', validators=[
                                     DataRequired(), equal_to('password')])
    gender = RadioField('Gender', validators=[DataRequired()], choices=[
                        ('male', 'male'), ('female', 'female')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember me')


class EditAccountForm(FlaskForm):
    description = StringField('Description', validators=[Length(max=200)])
    submit = SubmitField('Update')