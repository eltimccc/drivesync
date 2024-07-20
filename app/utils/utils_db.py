import os
import time
import shutil
from sqlalchemy import event

BACKUP_DIR = "db_backups"

import os
import time
import shutil
from sqlalchemy import event

BACKUP_DIR = "db_backups"
MAX_BACKUPS = 3

def create_backup(db_path):
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    all_backups = sorted(os.listdir(BACKUP_DIR))

    if len(all_backups) >= MAX_BACKUPS:
        oldest_backup = all_backups[0]
        os.remove(os.path.join(BACKUP_DIR, oldest_backup))

    backup_name = f"backup_{time.strftime('%d-%m-%Y-%H-%M')}_app.db"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    shutil.copy2(db_path, backup_path)
    print(f"Backup created at {backup_path}")

def register_event_listeners(app, db):
    @event.listens_for(db.session, 'before_commit')
    def before_commit(session):
        db_path = os.path.join(app.instance_path, app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", ""))
        create_backup(db_path)