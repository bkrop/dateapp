from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CreateMessageForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=1, max=300)])
    submit = SubmitField('Send')