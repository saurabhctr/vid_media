# app/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from .storage_management import manage_storage
from flask import current_app as app

def setup_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=lambda: manage_storage(app.config['VIDEO_STORAGE_PATH'], None), trigger="interval", minutes=5)
    scheduler.start()
