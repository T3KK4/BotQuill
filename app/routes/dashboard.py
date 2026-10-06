import os
import uuid
from functools import wraps
from app.extensions import db
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import current_user, login_required
from app.models import ContactInfo, Novel, Manuscript, BlogPost, Purchase, Message, WriterProfile
from app.forms import ManuscriptForm, NovelForm, BlogPostForm, WriterProfileForm, ContactInfoForm

dash_bp = Blueprint('dashboard', __name__)

# Decorator to ensure that the current user is a writer.
def writer_required(f):
    """Decorator to ensure that the current user is a writer."""
    @login_required
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_writer():
            flash('You do not have permission to access this page.', category='error')
            abort(403)  # Forbidden
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

 # Function that saves uploads
def save_upload(file, subfolder=''):
    """Save an uploaded file to the specified subfolder and return its relative path."""
    if not file:
        return None
    filename = secure_filename(file.filename)
    unique = f"{uuid.uuid4().hex[:8]}_{filename}"
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder, unique)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path)
    return os.path.join(subfolder, unique).replace('\\', '/')

    # Redirect to the writer login page.
@dash_bp.route('/login')
def login_redirect():
    return redirect(url_for('auth.writer_login'))

    # Main dashboard overview for the writer, showing stats and recent purchases
@dash_bp.route('/')
@login_required
@writer_required
def overview():
    """Dashboard overview for the writer."""
    stats = {
        'manuscripts': Manuscript.query.count(),
        'novels': Novel.query.count(),
        'posts': BlogPost.query.count(),
        'purchases': Purchase.query.count(),
        'unread_messages': Message.query.filter_by(is_read=False).count(),
        'sales': Purchase.query.with_entities(db.func.sum(Purchase.amount_paid)).scalar() or 0.0
    }
    
    recent_purchases = Purchase.query.order_by(Purchase.purchased_at.desc()).limit(5).all()
    return render_template('dashboard/overview.html', stats=stats, recent_purchases=recent_purchases)

# ---MANUSCRIPTS---

@dash_bp.route('/manuscripts')
@login_required
@writer_required
def manuscripts():
    """Display all manuscripts in the dashboard."""
    items = Manuscript.query.order_by(Manuscript.updated_at.desc()).all()
    return render_template('dashboard/manuscripts.html', items=items)

@dash_bp.route('/manuscripts/new', methods=['GET', 'POST'])
@dash_bp.route('/manuscripts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@writer_required
def edit_manuscript(id=None):
    """Create a new manuscript or edit an existing one."""
    item = Manuscript.query.get_or_404(id) if id else None
    form = ManuscriptForm(obj=item)
    if form.validate_on_submit():
        if not item:
            item = Manuscript()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash('Manuscript saved.', category='success')
        return redirect(url_for('dashboard.manuscripts'))
    return render_template('dashboard/edit_manuscript.html', form=form, manuscript=item)

@dash_bp.route('/manuscripts/<int:id>/delete', methods=['POST'])
@login_required
@writer_required
def delete_manuscript(id):
    """Delete a manuscript."""
    item = Manuscript.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Manuscript deleted.', category='success')
    return redirect(url_for('dashboard.manuscripts'))

# ---NOVELS---

@dash_bp.route('/novels')
@login_required
@writer_required
def novels():
    """Display all novels in the dashboard."""
    items = Novel.query.order_by(Novel.created_at.desc()).all()
    return render_template('dashboard/novels.html', novels=items)

@dash_bp.route('/novels/new', methods=['GET', 'POST'])
@dash_bp.route('/novels/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@writer_required
def edit_novel(id=None):
    """Create a new novel or edit an existing one."""
    item = Novel.query.get_or_404(id) if id else None
    form = NovelForm(obj=item)
    if form.validate_on_submit():
        if not item:
            item = Novel()
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash('Novel saved.', category='success')
        return redirect(url_for('dashboard.novels'))
    return render_template('dashboard/edit_novel.html', form=form, novel=item)

@dash_bp.route('/novels/<int:id>/delete', methods=['POST'])
@login_required
@writer_required
def delete_novel(id):
    """Delete a novel."""
    item = Novel.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Novel deleted.', category='success')
    return redirect(url_for('dashboard.novels'))


# ---BLOG POSTS---

@dash_bp.route('/blog-posts')
@login_required
@writer_required
def blog_posts():
    """Display all blog posts in the dashboard."""
    items = BlogPost.query.order_by(BlogPost.published_at.desc()).all()
    return render_template('dashboard/blog_posts.html', posts=items)


@dash_bp.route('/blog-posts/new', methods=['GET', 'POST'])
@dash_bp.route('/blog-posts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@writer_required
def edit_blog_post(id=None):
    """Create a new blog post or edit an existing one."""
    items = BlogPost.query.get_or_404(id) if id else None
    form = BlogPostForm(obj=items)
    if form.validate_on_submit():
        if not items:
            items = BlogPost()
        form.populate_obj(items)
        db.session.add(items)
        db.session.commit()
        flash('Blog post saved.', category='success')
        return redirect(url_for('dashboard.blog_posts'))
    return render_template('dashboard/edit_blog_post.html', form=form, post=items)

@dash_bp.route('/blog-posts/<int:id>/delete', methods=['POST'])
@login_required
@writer_required
def delete_blog_post(id):
    """Delete a blog post."""
    item = BlogPost.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Blog post deleted.', category='success')
    return redirect(url_for('dashboard.blog_posts'))

# ---SETTINGS---


@dash_bp.route('/settings', methods=['GET', 'POST'])
@login_required
@writer_required
def settings():
    """Display and update writer settings."""
    profile = WriterProfile.query.first()
    contact = ContactInfo.query.first()
    
    profile_form = WriterProfileForm(obj=profile)
    contact_form = ContactInfoForm(obj=contact)
    
    if 'save profile' in request.form and profile_form.validate_on_submit():
        if not profile:
            profile = WriterProfile()
        profile_form.populate_obj(profile)
        if profile_form.profile_photo.data:
            uploaded_photo = save_upload(profile_form.profile_photo.data, 'profile')
            if uploaded_photo is not None:
                profile.profile_photo = uploaded_photo
        db.session.add(profile)
        db.session.commit()
        flash('Profile updated.', category='success')
        return redirect(url_for('dashboard.settings'))
    
    if 'save contact' in request.form and contact_form.validate_on_submit():
        if not contact:
            contact = ContactInfo()
        contact_form.populate_obj(contact)
        db.session.add(contact)
        db.session.commit()
        flash('Contact info updated.', category='success')
        return redirect(url_for('dashboard.settings'))
    
    messages = Message.query.order_by(Message.created_at.desc()).limit(10).all()
    return render_template('dashboard/settings.html', profile_form=profile_form, contact_form=contact_form, messages=messages)


# Mark read messages

@dash_bp.route('/messages/<int:id>/mark-read', methods=['POST'])
@login_required
@writer_required
def mark_message_read(id):
    """Mark a message as read."""
    msg = Message.query.get_or_404(id)
    msg.is_read = True
    db.session.commit()
    flash('Message marked as read.', category='success')
    return redirect(url_for('dashboard.settings'))