from flask import Flask, request, jsonify, Blueprint
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
import functools

# Define the blueprint
user_blueprint = Blueprint('user', __name__)


# Constants for user roles
ROOT = 'root'
ADMIN = 'admin'
USER = 'user'


class User(UserMixin):
    def __init__(self, username, password, role=USER):
        self.username = username
        self.password = password
        self.role = role

    def get_id(self):
        return self.username


# Updated users with roles
users = {
    'root': User('root', 'su', ROOT),
    'admin': User('admin', 'admin', ADMIN),
    'user': User('user', 'user', USER),
}


# Decorator for role-based access control
def role_required(*roles, endpoint=None):
    def wrapper(fn):
        @login_required
        @functools.wraps(fn)  # 确保每个视图函数保持其原始名称
        def decorated_view(*args, **kwargs):
            if current_user.role not in roles:
                return jsonify({'message': 'Access denied'}), 403
            return fn(*args, **kwargs)

        decorated_view.__name__ = endpoint if endpoint else fn.__name__
        return decorated_view

    return wrapper


# @login_manager.user_loader
# def load_user(user_id):
#     return users.get(user_id)


# Authentication routes with role checks
@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = users.get(username)
    if user and password == user.password:
        login_user(user)
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Login failed'})


@user_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})


# Example of a protected route
@user_blueprint.route('/admin_only', methods=['GET'])
@role_required(ADMIN, ROOT)
def admin_only_route():
    return jsonify({'message': 'Welcome Admin!'})

