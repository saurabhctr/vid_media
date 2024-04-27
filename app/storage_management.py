# app/storage_management.py

import os
from .models import Video, LiveVideoBackup, db
from flask import current_app as app
from datetime import datetime

def manage_storage(folder, current_video_id):
    # Check storage and clean up if necessary
    if get_folder_size(folder) > 500 * 1024 * 1024:  # 500MB limit for primary storage
        cleanup_folder(folder, current_video_id)
    if get_folder_size(app.config['BACKUP_STORAGE_PATH']) > 500 * 1024 * 1024:  # 500MB limit for backup storage
        cleanup_backup_folder(app.config['BACKUP_STORAGE_PATH'])

def cleanup_folder(folder, exclude_id):
    # Exclude the video currently being stored (if any)
    videos = Video.query.filter(Video.id != exclude_id).all()
    for video in videos:
        if not is_currently_streaming(video.id):
            os.remove(os.path.join(folder, video.path))
            db.session.delete(video)
    db.session.commit()

def cleanup_backup_folder(folder):
    # Delete 50% of the oldest files in the backup folder
    backups = sorted(LiveVideoBackup.query.all(), key=lambda x: x.start_time)
    delete_count = len(backups) // 2
    for backup in backups[:delete_count]:
        os.remove(os.path.join(folder, backup.path))
        db.session.delete(backup)
    db.session.commit()

def get_folder_size(folder):
    # Calculate total size of files in the given folder
    return sum(os.path.getsize(os.path.join(folder, f)) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)))

def is_currently_streaming(video_id):
    # Placeholder for checking if a video is currently being streamed
    # This should interface with whatever logic determines if a stream is active
    return False

def manage_live_video_backup(video):
    # Create a backup of the video and start a new segment if needed
    current_time = datetime.now()
    original_path = video.path
    backup_path = os.path.join(app.config['BACKUP_STORAGE_PATH'], os.path.basename(original_path))
    shutil.copy(original_path, backup_path)
    backup_entry = LiveVideoBackup(original_video_id=video.id, path=backup_path, segment_time=current_time, start_time=video.start_time, end_time=current_time)
    db.session.add(backup_entry)
    db.session.commit()
