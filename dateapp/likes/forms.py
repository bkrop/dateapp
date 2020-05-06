from flask_wtf import FlaskForm
from wtforms import SubmitField

class LikePerson(FlaskForm):
    submit = SubmitField('Like')
    dislike = SubmitField('Dislike')