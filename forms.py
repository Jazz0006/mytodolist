from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])