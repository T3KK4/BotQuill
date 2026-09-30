from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, TextAreaField, DecimalField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Optional, NumberRange, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'Confirm password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')],
    )
    submit = SubmitField('Sign Up')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ManuscriptForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    genre = StringField('genre')
    status = SelectField('Status', choices=[
        ('Draft': 'Draft'), 
        ('Editing': 'Editing'), 
        ('Revision': 'Revision'), 
        ('complete': 'complete')], default='Draft')
    progress_percent = IntegerField()
    word_count = IntegerField()
    target_word_count = IntegerField()
    notes = TextAreaField()
    submit = SubmitField('Save')