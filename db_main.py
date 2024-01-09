from flask import Flask, jsonify, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoORM(db.Model):
    __tablename__ = "video"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    m3u8_url = db.Column(db.String(255), nullable=True)
    create_at = db.Column(db.DateTime, default=datetime.now)

# API endpoints
@app.route('/videos', methods=['GET'])
def get_videos():
    videos = VideoORM.query.all()
    return jsonify([video.__dict__ for video in videos])


@app.route('/videos', methods=['POST'])
def create_video():
    data = request.get_json()
    video = VideoORM(name=data['name'], url=data['url'], m3u8_url=data['m3u8_url'])
    db.session.add(video)
    db.session.commit()
    return jsonify({'message': 'Video created successfully'})


@app.route('/videos/<int:video_id>', methods=['GET'])
def get_video(video_id):
    video = VideoORM.query.get(video_id)
    if video:
        return jsonify(video.__dict__)
    else:
        return jsonify({'message': 'Video not found'})


@app.route('/videos/<int:video_id>', methods=['PUT'])
def update_video(video_id):
    data = request.get_json()
    video = VideoORM.query.get(video_id)
    if video:
        video.name = data['name']
        video.url = data['url']
        video.m3u8_url = data['m3u8_url']
        db.session.commit()
        return jsonify({'message': 'Video updated successfully'})
    else:
        return jsonify({'message': 'Video not found'})


@app.route('/videos/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    video = VideoORM.query.get(video_id)
    if video:
        db.session.delete(video)
        db.session.commit()
        return jsonify({'message': 'Video deleted successfully'})
    else:
        return jsonify({'message': 'Video not found'})


if __name__ == '__main__':
    app.run(debug=True)
