from flask import Flask, render_template, send_from_directory
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from db_main import db

from video import video_blueprint, VideoORM  # 导入 video 蓝图和 VideoORM
from user import user_blueprint  # 导入 user 蓝图

app = Flask(__name__)

# 配置数据库
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["UPLOAD_FOLDER"] = "file_storage/video"

# 设置secret_key
app.config["SECRET_KEY"] = "8f42a73054b1749f8f58848be5e6502c"

# 初始化 db
db.init_app(app)

# 初始化 Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'user.login'  # 更新登录视图的端点

# 注册蓝图
app.register_blueprint(user_blueprint)
app.register_blueprint(video_blueprint)

# 在应用程序上下文中检查并创建数据库表
with app.app_context():
    if not inspect(db.engine).has_table('video'):
        db.create_all()

@login_manager.user_loader
def load_user(user_id):
    # 从 user.py 导入的用户字典中获取用户
    from user import users
    return users.get(user_id)

@app.route('/file_storage/<path:filename>')
def custom_static(filename):
    return send_from_directory('file_storage', filename)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
