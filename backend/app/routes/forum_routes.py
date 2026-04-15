from flask import Blueprint, request, jsonify
from app.models.forum import ForumPost, ForumComment
from app import db

forum_bp = Blueprint('forum_routes', __name__)

@forum_bp.route('/api/forum/posts', methods=['GET'])
def get_posts():
    """Get all forum posts. Feature 4."""
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200

@forum_bp.route('/api/forum/posts', methods=['POST'])
def create_post():
    data = request.json
    # hardcoded user_id for demonstration if omitted
    user_id = data.get('user_id', 1) 
    
    new_post = ForumPost(
        user_id=user_id,
        title=data.get('title'),
        body=data.get('body'),
        category=data.get('category')
    )
    db.session.add(new_post)
    db.session.commit()
    
    return jsonify(new_post.to_dict()), 201

@forum_bp.route('/api/forum/posts/<int:post_id>/comments', methods=['GET', 'POST'])
def handle_comments(post_id):
    if request.method == 'GET':
        comments = ForumComment.query.filter_by(post_id=post_id).order_by(ForumComment.created_at.asc()).all()
        return jsonify([c.to_dict() for c in comments]), 200
        
    elif request.method == 'POST':
        data = request.json
        user_id = data.get('user_id', 1)
        new_comment = ForumComment(
            post_id=post_id,
            user_id=user_id,
            content=data.get('content')
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment.to_dict()), 201
