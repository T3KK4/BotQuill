import os
from flask import Flask

from app.extensions import db, login_manager, migrate
from app.config import Config
from app.models import User, WriterProfile, ContactInfo


def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config_class)
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # type: ignore
    login_manager.login_message_category = 'success'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.dashboard import dash_bp as dashboard_bp
    from .routes.payments import payment_bp
    
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(payment_bp, url_prefix='/payments')
    
    with app.app_context():
        db.create_all()
        _seed_writer_and_site_data(app)
    return app

def _seed_writer_and_site_data(app):
    """Create the single writer account and default site data if none exists."""
        
    if not User.query.filter_by(role='writer').first():
        writer = User(
            username=app.config['WRITER_USERNAME'],    # type: ignore 
            email=app.config['WRITER_EMAIL'],          # type: ignore  
            role='writer'                              # type: ignore  
        )
        writer.set_password(app.config['WRITER_PASSWORD'])
        db.session.add(writer)
        db.session.commit()
            
    if not WriterProfile.query.first():
        profile = WriterProfile(
            full_name='Bot Cynthia',    # type: ignore 
            tagline='Novelist & Storyteller',   # type: ignore 
            bio='Welcome to BotQuill. Update this bio from your dashboard.' # type: ignore 
        )
        db.session.add(profile)
            
    if not ContactInfo.query.first():
        contact = ContactInfo(
            display_email = 'cynthbot6@gmail.com',    # type: ignore 
            contact_message = app.config['DEFAULT_MESSAGE']     # type: ignore 
        )
        db.session.add(contact)
            
    db.session.commit()