from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('landing/index.html')

@main_bp.route('/blog')
def blog():
    return render_template('blog/blog.html', text="Test Text")

@main_bp.route('/books')
def books():
    return render_template('book/books.html')

@main_bp.route('/user/<user_id>')
def user_page(user_id):
    return render_template('user/user.html', user_id=user_id)