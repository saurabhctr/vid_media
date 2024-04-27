# app/models.py

from . import db
from datetime import datetime

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), unique=True)
    user_id = db.Column(db.String(255))
    session_id = db.Column(db.String(255))
    start_time = db.Column(db.DateTime, default=datetime.now)
    end_time = db.Column(db.DateTime, nullable=True)

class LiveVideoBackup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    path = db.Column(db.String(255), unique=True)
    segment_time = db.Column(db.DateTime, default=datetime.now)
    start_time = db.Column(db.DateTime, default=datetime.now)
    end_time = db.Column(db.DateTime, nullable=True)
