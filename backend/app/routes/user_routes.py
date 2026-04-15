from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.notification import UserAlert
from app import db

user_bp = Blueprint('user_routes', __name__)

@user_bp.route('/api/users/<int:user_id>', methods=['GET', 'PUT'])
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'GET':
        return jsonify(user.to_dict()), 200
        
    elif request.method == 'PUT':
        data = request.json
        user.age = data.get('age', user.age)
        user.occupation = data.get('occupation', user.occupation)
        user.income = data.get('income', user.income)
        user.category = data.get('category', user.category)
        user.language_preference = data.get('language_preference', user.language_preference)
        db.session.commit()
        return jsonify(user.to_dict()), 200

@user_bp.route('/api/users/<int:user_id>/notifications', methods=['GET'])
def get_notifications(user_id):
    """Get active notifications for user."""
    alerts = UserAlert.query.filter_by(user_id=user_id).order_by(UserAlert.created_at.desc()).all()
    return jsonify([alert.to_dict() for alert in alerts]), 200
