from flask import Blueprint, render_template
from flask_login import login_required
from app.models import User

main_bp = Blueprint('main', __name__)

# The main landing page that welcomes a user when they log into the site
@main_bp.route('/')
def index():
    return render_template('landing/index.html')

# The main blog area for when a user chooses to explore blog posts
@main_bp.route('/blog')
def blog():
    return render_template('blog/blog.html', text="Test Text")

# The book display page/library when a user chooses to explore novels
@main_bp.route('/books')
def books():
    return render_template('book/books.html')

# The user display for when a User properly logs in after visiting our landing page
@main_bp.route('/user/<user_id>')
@login_required
def user_page(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    return render_template('user/user.html', username=user.username) # type: ignore