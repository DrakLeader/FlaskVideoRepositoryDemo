from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

users = {
    'root': User('root', 'root'),
    'admin': User('admin', 'admin'),
    'user': User('user', 'user'),
}

class UserGroup:
    def __init__(self, group_name, users):
        self.group_name = group_name
        self.users = users

user_group = UserGroup('admins', [users['root'], users['admin']])

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# 鉴权路由
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = users.get(username)
    if user and password == 'password':
        login_user(user)
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Login failed'})

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})
