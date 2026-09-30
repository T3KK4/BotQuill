from app.extensions import db
from flask_login import UserMixin
from sqlalchemy import String, Text, DateTime, Numeric, Boolean, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime
from typing import Optional, List
import uuid


# User Model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default='reader') # reader or writer are the two roles
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # reverse relationship between user and [posts, novels] 
    posts: Mapped[List["BlogPost"]] = relationship(back_populates="user", lazy="dynamic", passive_deletes=True)
    novels: Mapped[List["Novel"]] = relationship(back_populates="user", lazy="dynamic", passive_deletes=True)
    
    # Methods for setting and checking
    def set_password(self, password) -> (str | None):
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
    created_at: Mapped[datetime] = mapped_column(
                                                    DateTime(timezone=True), 
                                                    server_default=func.now(), 
                                                    onupdate=func.now()
                                                )
    
    @property
    def progress_display(self) -> (float | int):
        return min(max(self.progress_percent, 0), 100)



# Novel Model
class Novel(db.model):
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
    
    # reverse relationship between novel and purchases 
    purchases: Mapped[List["Purchase"]] = relationship(back_populates="novels", lazy="dynamic", passive_deletes=True)
    
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
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
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
    fullname: Mapped[str] = mapped_column(String(100), default='')
    tagline: Mapped[str] = mapped_column(String(250), default='')
    bio: Mapped[str] = mapped_column(Text)
    skills: Mapped[str] = mapped_column(Text, default='')
    profile_photo: Mapped[str] = mapped_column(String(300))
    resume_link: Mapped[str] = mapped_column(String(300))
    


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
    


# Purchase records
class Purchase(db.Model):
    __tablename__ = 'purchases'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_email: Mapped[str] = mapped_column(String(100), nullable=False)
    stripe_payment_intent_id: Mapped[str] = mapped_column(String(100))
    amount_paid: Mapped[int] = mapped_column(Numeric(10, 2))
    purchased_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    download_token: Mapped[str] = mapped_column(String(100), unique=True, default=lambda: str(uuid.uuid4()))
    is_downloaded: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Foreign keys
    novel_id: Mapped[int] = mapped_column(ForeignKey('novels.id', ondelete='CASCADE'), nullable=False, index=True)
    novel: Mapped["Novel"] = relationship(back_populates="purchases")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), nullable=False, index=True)
    user: Mapped["User"] = relationship(back_populates="purchases")