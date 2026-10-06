from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Purchase, User

payment_bp = Blueprint('payment', __name__)