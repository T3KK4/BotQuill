from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    return "<h2>Logout Page</h2>"


@auth_bp.route('/register')
def register():
    return render_template('register.html')


@auth_bp.route('/writer-login')
def writer_login():
    return "<h2>Writer Login Page</h2>"