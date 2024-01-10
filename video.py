from datetime import datetime
import os
import hashlib
import os
import shutil
import pathlib
from flask import Flask, render_template, request, jsonify
from sqlalchemy import inspect
from flask import Blueprint
from flask import current_app as video
from user import role_required
from db_main import db

# Define the blueprint
video_blueprint = Blueprint('video', __name__)


class VideoORM(db.Model):
    __tablename__ = "video"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    m3u8_url = db.Column(db.String(255), nullable=True)
    create_at = db.Column(db.DateTime, default=datetime.now)
    is_public = db.Column(db.Boolean, default=True)


@video_blueprint.route('/upload_video', methods=['GET'])
@role_required('root', 'admin', endpoint='video_upload_video')
def upload_video():
    return render_template("video_upload.html")


@video_blueprint.route('/video_upload', methods=['POST'])
@role_required('root', 'admin', endpoint='video_video_upload')
def upload_video2():
    file = request.files["file"]
    if file:
        """Recieve video file and book in DB"""
        filename = file.filename
        # read file content
        content = file.read()
        # get file md5
        hex_name = hashlib.md5(content).hexdigest()
        # get file suffix
        suffix = pathlib.Path(filename).suffix
        # new file name with previous suffix
        new_filename = hex_name + suffix
        print("new_filename", new_filename)
        upload_dir = pathlib.Path(video.config["UPLOAD_FOLDER"])
        os.makedirs(upload_dir, exist_ok=True)
        # write file
        new_path = upload_dir.joinpath(new_filename)
        open(new_path, mode="wb").write(content)

        """convert to m3u8"""
        # construct m3u8 dir
        m3u8_path = upload_dir.parent.joinpath("m3u8")
        if not m3u8_path.exists():
            m3u8_path.mkdir()

        current_dir = m3u8_path.joinpath(hex_name)
        if not current_dir.exists():
            current_dir.mkdir()

        # generate ts file
        cli1 = f"ffmpeg -y -i {new_path} -vcodec copy -acodec copy -bsf:v h264_mp4toannexb {str(current_dir)}/index.ts"
        os.system(cli1)
        print("cli1:", cli1)
        # split ts and index m3u8
        cli2 = f'ffmpeg -i {str(current_dir)}/index.ts -c copy -map 0 -f segment -segment_list {str(current_dir)}/index.m3u8 -segment_time 10 "{str(current_dir)}/index-%04d.ts"'
        os.system(cli2)
        print("cli2", cli2)

        # Init ORM
        mv = VideoORM()
        mv.url = "/" + str(new_path)
        mv.name = filename
        mv.m3u8_url = "/" + str(current_dir) + "/index.m3u8"
        db.session.add(mv)
        db.session.commit()

    return {"code": 0, "msg": "上传视频成功"}


@video_blueprint.route('/delete_video/<int:video_id>', methods=['POST'])
@role_required('root', 'admin', endpoint='video_delete_video')
def delete_video(video_id):
    video = VideoORM.query.get(video_id)
    if video:
        # Delete video
        video_file_path = video.url.lstrip('/')
        m3u8_file_path = video.m3u8_url.lstrip('/')
        ts_folder_path = os.path.dirname(m3u8_file_path)

        try:
            if os.path.exists(video_file_path):
                os.remove(video_file_path)
            if os.path.exists(m3u8_file_path):
                shutil.rmtree(ts_folder_path)
        except Exception as e:
            return {"code": 1, "msg": f"删除文件时出错: {str(e)}"}

        # delete DB record
        db.session.delete(video)
        db.session.commit()
        return {"code": 0, "msg": "视频删除成功"}
    return {"code": 1, "msg": "视频未找到"}

@video_blueprint.route('/rename_video/<int:video_id>', methods=['POST'])
@role_required('root', 'admin', endpoint='video_rename_video')
def rename_video(video_id):
    data = request.get_json()
    new_name = data.get('newName')
    video = VideoORM.query.get(video_id)

    if video and new_name:
        video.name = new_name
        db.session.commit()
        return {"code": 0, "msg": "视频重命名成功"}
    return {"code": 1, "msg": "视频未找到或新名称无效"}


@video_blueprint.route("/manage", methods=["GET"])
def hello_world():
    inspector = inspect(db.engine)
    if not inspector.has_table("video"):
        db.create_all()

    q = db.select(VideoORM)
    video_list = db.session.execute(q).scalars()
    return render_template("manage.html", video_list=video_list)


@video_blueprint.route("/video_play")
def video_play():
    vid = request.args.get("video_id")
    video = VideoORM.query.get(vid)
    return render_template("video_play.html", url=video.m3u8_url.replace('\\', '/'))

@video_blueprint.route('/search_videos', methods=['GET'])
def search_videos():
    search_query = request.args.get('query', '')
    search_results = VideoORM.query.filter(VideoORM.name.contains(search_query)).all()
    return jsonify([{'id': video.id, 'name': video.name, 'create_at': video.create_at.strftime('%Y-%m-%d %H:%M:%S')} for video in search_results])
