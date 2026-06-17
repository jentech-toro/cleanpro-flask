from datetime import datetime
from app.models.product import db

class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    total = db.Column(db.Float, nullable=False)

    items = db.Column(db.Text, nullable=False)  # JSON o texto

    created_at = db.Column(db.DateTime, default=datetime.utcnow)