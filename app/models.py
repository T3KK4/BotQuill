from app.extensions import db
from flask_login import UserMixin
from sqlalchemy import String, Text, DateTime, Numeric, Boolean, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime, timezone, timedelta
from typing import Optional, List
import uuid


# User Model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default='reader') # reader or writer are the two roles
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # reverse relationships
    posts: Mapped[List["BlogPost"]] = relationship(back_populates="user", lazy="dynamic", passive_deletes=True)
    novels: Mapped[List["Novel"]] = relationship(back_populates="user", lazy="dynamic", passive_deletes=True)
    purchases: Mapped[List["Purchase"]] = relationship(back_populates="user", lazy="dynamic", passive_deletes=True)
    purchase_event: Mapped[List["PurchaseEvent"]] = relationship(back_populates="user", lazy="dynamic", passive_deletes=True)
    
    # Methods for setting and checking
    def set_password(self, password) -> (None):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)
    
    def is_writer(self) -> bool:
        return self.role == 'writer'



# Manuscript Model  
class Manuscript(db.Model):
    __tablename__ = 'manuscripts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author_name: Mapped[str] = mapped_column(String(50), default='')
    genre: Mapped[str] = mapped_column(String(30))
    cover_photo: Mapped[str] = mapped_column(String(300))
    status: Mapped[str] = mapped_column(String(50), default='Draft')
    progress_percent: Mapped[int] = mapped_column(Integer, default=0)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    target_word_count: Mapped[int] = mapped_column(Integer, default=80_000)
    notes: Mapped[str] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    @property
    def progress_display(self) -> (float | int):
        return min(max(self.progress_percent, 0), 100)



# Novel Model
class Novel(db.Model):
    __tablename__ = 'novels'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author_name: Mapped[str] = mapped_column(String(50), default='')
    completion_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    cover_photo: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00)
    ebook_file: Mapped[str] = mapped_column(String(300))
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign Keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), nullable=False, index=True)
    user: Mapped["User"] = relationship(back_populates="novels")
    
    # reverse relationships
    purchases: Mapped[List["Purchase"]] = relationship(back_populates="novel", lazy="dynamic", passive_deletes=True)
    purchase_event: Mapped[List["PurchaseEvent"]] = relationship(back_populates="novel", lazy="dynamic", passive_deletes=True)
    # Property Methods
    @property
    def formatted_price(self) -> str:
        return f"${self.price:.2f}"



# Blog Post Model
class BlogPost(db.Model):
    __tablename__ = 'blog_post'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[str] = mapped_column(String(400))
    cover_image: Mapped[str] = mapped_column(String(300))
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
     # relationship between users and posts 
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), nullable=False, index=True) 
    user: Mapped["User"] = relationship(back_populates="posts")
    
    def generate_slug(self) -> str:
        base = self.title.lower().replace(' ', '-')
        base = ''.join(c for c in base if c.isalnum() or c == '-')
        slug = base
        counter = 1
        while BlogPost.query.filter_by(slug=slug).first():
            slug = f"{base}-{counter}"
            counter += 1
        return slug



# Writer Model | Admin
class WriterProfile(db.Model):
    __tablename__ = 'writer_profile'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), default='')
    tagline: Mapped[str] = mapped_column(String(250), default='')
    bio: Mapped[str] = mapped_column(Text, nullable=False)
    skills: Mapped[str] = mapped_column(Text, default='', nullable=True)
    profile_photo: Mapped[str] = mapped_column(String(300), nullable=True)
    resume_link: Mapped[str] = mapped_column(String(300), nullable=True)
    


# Contact Information Model
class ContactInfo(db.Model):
    __tablename__ = 'contact_info'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    display_email: Mapped[str] = mapped_column(String(100), default='')
    phone: Mapped[str] = mapped_column(String(30), default='')
    location: Mapped[str] = mapped_column(String(100), default='')
    twitter: Mapped[str] = mapped_column(String(100), default='')
    linkedin: Mapped[str] = mapped_column(String(100), default='')
    contact_message: Mapped[str] = mapped_column(Text, default='')



# Message Model
class Message(db.Model):
    __tablename__ = 'messages'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), default='')
    email: Mapped[str] = mapped_column(String(100), default='')
    subject: Mapped[str] = mapped_column(String(200), default='')
    body: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    


# Purchase records
class Purchase(db.Model):
    __tablename__ = 'purchases'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_email: Mapped[str] = mapped_column(String(100), nullable=False)
    stripe_payment_intent_id: Mapped[str] = mapped_column(String(100))
    amount_paid: Mapped[float] = mapped_column(Numeric(10, 2))
    purchased_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    download_token: Mapped[str] = mapped_column(String(100), unique=True, default=lambda: str(uuid.uuid4()))
    is_downloaded: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Foreign keys
    novel_id: Mapped[int] = mapped_column(ForeignKey('novels.id', ondelete='CASCADE'), nullable=False, index=True)
    novel: Mapped["Novel"] = relationship(back_populates="purchases")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), nullable=False, index=True)
    user: Mapped["User"] = relationship(back_populates="purchases")
    
# Dashboard Analytics System

class PageView(db.Model):
    """Tracks every view of a blog post or novel detail page"""
    __tablename__ = 'page_view'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    page_type: Mapped[str] = mapped_column(String(20), nullable=False)  # 'blog' or 'novel'
    page_id: Mapped[int] = mapped_column(Integer, nullable=False)   # blog_post.id or novel.id
    ip_address: Mapped[str] = mapped_column(String(45))
    user_agent: Mapped[str] = mapped_column(String(255))
    viewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), nullable=False, index=True)
    
    
    @staticmethod
    def get_daily_counts(page_type, days=30):
        """Return list of (date_str, count) for the last N days."""
        since = datetime.now(timezone.utc) - timedelta(days=days)
        from sqlalchemy import func, cast, Date
        rows = db.session.query(
            cast(PageView.viewed_at, Date).label('day'),
            func.count(PageView.id).label('cnt')
        ).filter(
            PageView.page_type == page_type,
            PageView.viewed_at >= since 
        ).group_by('day').order_by('day').all()
        return rows
    
class PurchaseEvent(db.Model):
    """Track every step of the purchase funnel."""
    __tablename__ = 'purchase_event'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    stripe_session_id: Mapped[str] = mapped_column(String(100))
    ip_address: Mapped[str] = mapped_column(String(45))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), nullable=False, index=True)
    user: Mapped["User"] = relationship(back_populates="purchase_event")
    novel_id: Mapped[int] = mapped_column(ForeignKey("novels.id", ondelete='CASCADE'), nullable=False, index=True)
    novel: Mapped["Novel"] = relationship(back_populates="purchase_event")
    
    @staticmethod
    def get_daily_counts(page_type, days=30):
        """Return list of (date_str, count) for the last N days."""
        since = datetime.now(timezone.utc) - timedelta(days=days)
        from sqlalchemy import func, cast, Date
        rows = db.session.query(
            cast(PageView.viewed_at, Date).label('day'),
            func.count(PageView.id).label('cnt')
        ).filter(
            PageView.page_type == page_type,
            PageView.viewed_at >= since 
        ).group_by('day').order_by('day').all()
        return rows
    
    @staticmethod
    def get_top_novels_by_event(event_type, limit=5):
        from sqlalchemy import func
        rows = db.session.query(
            Novel.title,
            func.count(PurchaseEvent.id).label('cnt')
        ).join(PurchaseEvent, Novel.id==PurchaseEvent.novel_id)\
            .filter(PurchaseEvent.event_type==event_type)\
            .group_by(Novel.id)\
            .order_by(func.count(PurchaseEvent.id).desc())\
            .limit(limit).all()
        return rows
    
class SiteVisit(db.Model):
    """Tracks general home page and site visits"""  
    __tablename__ = 'site_visit'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String(100))
    ip_address: Mapped[str] = mapped_column(String(45))
    visited_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign Key
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), nullable=True, index=True)
    
    # methods
    @staticmethod
    def get_daily_counts(days=30):
        """Return list of (date_str, count) for the last N days."""
        since = datetime.now(timezone.utc) - timedelta(days=days)
        from sqlalchemy import func, cast, Date
        rows = db.session.query(
            cast(SiteVisit.visited_at, Date).label('day'),
            func.count(SiteVisit.id).label('cnt')
        ).filter(SiteVisit.visited_at >= since)\
        .group_by('day').order_by('day').all()
        return rows 