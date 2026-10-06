from decimal import Decimal
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, TextAreaField, DecimalField, PasswordField, SubmitField, SelectField, DateField, BooleanField
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
    title = StringField('Title', validators=[DataRequired()])
    genre = StringField('Genre')
    status = SelectField('Status', choices=[
        ('Draft', 'Draft'), 
        ('Editing', 'Editing'), 
        ('Revision', 'Revision'), 
        ('complete', 'complete')], default='Draft')
    progress_percent = IntegerField('Progress %', validators=[NumberRange(0, 100)], default=0)
    word_count = IntegerField('Current Word Count', default=0)
    target_word_count = IntegerField('Target Word Count', default=0)
    notes = TextAreaField('Notes')
    submit = SubmitField('Save')
    
class NovelForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author_name = StringField('Author Name')
    completion_date = DateField('Completion Date', format='%Y-%m-%d', validators=[Optional()])
    cover_photo = FileField('Cover Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only'), DataRequired()])
    description = TextAreaField('Description')
    price = DecimalField('Price (USD)', places=2, default=Decimal(0.00))
    ebook_file = FileField('E-Book File', validators=[FileAllowed(['pdf', 'epub', 'mobi'], 'E-Books only')])
    is_published = BooleanField('Published')
    Submit = SubmitField('Add Novel')
    
class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    excerpt = TextAreaField('Excerpt (Optional)')
    cover_image = FileField('Cover Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only')])
    is_published = BooleanField('Published')
    published_at = DateField('Published Date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Post')
    
class WriterProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    tagline = StringField('Tagline')
    bio = TextAreaField('Writer Bio')
    skills = TextAreaField('Skills (comma separated)')
    profile_photo = FileField('Profile Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only')])
    resume_link = StringField('Resume/CV Link')
    submit = SubmitField('Update Profile')
    
class ContactInfoForm(FlaskForm):
    display_email = StringField('Public Email')
    phone = StringField('Phone Number')
    location = StringField('Public Address')
    twitter = StringField('Twitter/X (profile link)')
    linkedin = StringField('LinkedIn')
    contact_message = TextAreaField('Contact Page Introduction')
    submit = SubmitField('Update Contact Info')