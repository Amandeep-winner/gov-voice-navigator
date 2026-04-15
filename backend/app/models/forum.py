from app import db
from datetime import datetime

class ForumPost(db.Model):
    __tablename__ = 'forum_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    upvotes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Establish relationship for easier querying
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user.name,
            'is_official': self.user.is_official,
            'title': self.title,
            'body': self.body,
            'category': self.category,
            'upvotes': self.upvotes,
            'created_at': self.created_at.isoformat()
        }

class ForumComment(db.Model):
    __tablename__ = 'forum_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('ForumPost', backref=db.backref('comments', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_name': self.user.name,
            'is_official': self.user.is_official,
            'content': self.content,
            'upvotes': self.upvotes,
            'created_at': self.created_at.isoformat()
        }
