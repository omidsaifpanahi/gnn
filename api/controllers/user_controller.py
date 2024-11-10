from flask import Blueprint, jsonify
from api.middlewares.auth_user import auth_user
from api.models.user import UserModel

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard', methods=['GET'])
@auth_user
def user_dashboard():
    return jsonify({'message': 'داشبورد کاربر'}), 200