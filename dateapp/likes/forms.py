from flask_wtf import FlaskForm
from wtforms import SubmitField

class LikePerson(FlaskForm):
    submit = SubmitField('Like')
    
class DislikePerson(FlaskForm):
    submit = SubmitField('Dislike')