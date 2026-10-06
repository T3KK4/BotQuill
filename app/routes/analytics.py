from datetime import datetime, timedelta
from collections import defaultdict
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from sqlalchemy import func, cast, Date

from app.models import PageView, PurchaseEvent, SiteVisit, Novel, BlogPost, Purchase
from app.routes.dashboard import writer_required
from app.extensions import db

bp = Blueprint('analytics', __name__, url_prefix='/dashboard/analytics')

