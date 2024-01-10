from flask import Flask, render_template, send_from_directory
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from db_main import db

from video import video_blueprint, VideoORM
from user import user_blueprint

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["UPLOAD_FOLDER"] = "file_storage/video"

# set up secret_key
app.config["SECRET_KEY"] = "8f42a73054b1749f8f58848be5e6502c"

# init db
db.init_app(app)

# Init Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'user.login'  # Update the login view

# Register blueprints
app.register_blueprint(user_blueprint)
app.register_blueprint(video_blueprint)

# Create database tables if they don't exist
with app.app_context():
    if not inspect(db.engine).has_table('video'):
        db.create_all()

@login_manager.user_loader
def load_user(user_id):
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
