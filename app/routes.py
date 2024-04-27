# app/routes.py

from flask import current_app as app, request, jsonify
from werkzeug.utils import secure_filename
from . import db
from .models import Video
from .storage_management import manage_storage

@app.route('/upload_video', methods=['POST'])
def upload_video():
    session_id = request.headers.get('X-Session-ID')
    video = request.files['video']
    filename = secure_filename(video.filename)
    video_path = os.path.join(app.config['VIDEO_STORAGE_PATH'], filename)
    video.save(video_path)
    new_video = Video(path=video_path, user_id='user123', session_id=session_id)
    db.session.add(new_video)
    db.session.commit()
    manage_storage(app.config['VIDEO_STORAGE_PATH'], new_video.id)
    return jsonify({'message': 'Video saved successfully', 'video_id': new_video.id})
