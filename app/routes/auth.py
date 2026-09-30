from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user
from app.forms import LoginForm, RegisterForm
from app.models import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.user_page', user_id=current_user.id))
    
    login_form = LoginForm()
    register_form = RegisterForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user)
            return redirect(url_for('main.user_page', user_id=user.id))
        flash('Invalid username or Password!', category='error')
    return render_template('auth/register.html', user=current_user, login_form=login_form, register_form=register_form)


@auth_bp.route('/logout')
@login_required
def logout():
    return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    login_form=LoginForm()
    register_form=RegisterForm()
    if register_form.validate_on_submit():
        if User.query.filter((User.username == register_form.username.data) | (User.email == register_form.email.data)).first():
            flash('user name or email already exists in database', category='error')
            return redirect(url_for('auth.login'))
            
        user = User(username=register_form.username.data, email=register_form.email.data) # type: ignore
        user.set_password(register_form.password.data)
        flash('Registration successful!', category='success')
        login_user(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.user_page', user_id=user.id))
    return render_template('auth/register.html', login_form=login_form, register_form=register_form)


@auth_bp.route('/writer-login')
def writer_login():
    return "<h2>Writer Login Page</h2>"
