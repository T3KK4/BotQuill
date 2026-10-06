from app.extensions import db
from app.models import WriterProfile, BlogPost, Novel
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import User, PageView, SiteVisit

    # Helper function to log page views
def _log_page_view(page_type, page_id):
    """fire-and-forget page logging"""
    try:
        pv = PageView(
            page_type=page_type,    # type: ignore
            page_id=page_id,    # type: ignore
            user_id=current_user.id if current_user.is_authenticated else None, # type: ignore
            ip_address=request.remote_addr, # type: ignore
            user_agent=request.user_agent.string[:250] if request.user_agent else None  # type: ignore
        )
        db.session.add(pv)
        db.session.commit()
    except Exception:
        db.session.rollback()
    
def _log_site_visit(path='/'):
    """logger to keep track of site visits"""
    try:
        sv = SiteVisit(
            path=path,  # type: ignore
            user_id=current_user.id if current_user.is_authenticated else None, # type: ignore
            ip_address=request.remote_addr  # type: ignore
        )
        db.session.add(sv)
        db.session.commit()
    except Exception:
        db.session.rollback()

main_bp = Blueprint('main', __name__)

# The main landing page that welcomes a user when they log into the site
@main_bp.route('/')
def index():
    _log_site_visit('/')
    
    profile = WriterProfile.query.first()
    novels = Novel.query.filter_by(is_published=True).order_by(Novel.created_at.desc()).limit(6).all()
    posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc()).limit(4).all()
    return render_template('landing/index.html', profile=profile, novels=novels, posts=posts)

# The main blog area for when a user chooses to explore blog posts
@main_bp.route('/blog')
def blog():
    return render_template('blog/blog.html')

# The main blog post the user reads
@main_bp.route('/blog/<slug>')
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    _log_page_view('blog', post.id)
    return render_template('blog/blog_post.html', post=post)

# The book display page/library when a user chooses to explore novels
@main_bp.route('/novels')
def novels():
    return render_template('book/novels.html')

# The book detail page where a user can read details and preview a book
@main_bp.route('/novels/<int:id>')
@login_required
def novel_detail(id):
    novel = Novel.query.filter_by(id=id, is_published=True).first_or_404()
    _log_page_view('novel', novel.id)
    return render_template('book/novel_detail.html', novel=novel)

# The user display for when a User properly logs in after visiting our landing page
@main_bp.route('/user/<user_id>')
@login_required
def user_page(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    return render_template('user/user.html', username=user.username) # type: ignore