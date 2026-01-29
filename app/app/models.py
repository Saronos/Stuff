from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class URL(db.Model):
    __tablename__ = 'urls'
    
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))
    clicks = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_code': self.short_code,
            'short_url': f"{self.short_url}",
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'clicks': self.clicks
        }
    
    @property
    def short_url(self):
        from flask import current_app
        base_url = current_app.config.get('BASE_URL', 'http://localhost:5000')
        return f"{base_url}/{self.short_code}"