from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # Simple stand-in for auth
    
    # Profile data for scheme matching
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(100))
    income = db.Column(db.Float)
    category = db.Column(db.String(50)) # e.g. General, SC, ST, OBC
    
    # Settings
    language_preference = db.Column(db.String(20), default="en")
    
    # Flags
    is_official = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'occupation': self.occupation,
            'income': self.income,
            'category': self.category,
            'language': self.language_preference,
            'is_official': self.is_official
        }
