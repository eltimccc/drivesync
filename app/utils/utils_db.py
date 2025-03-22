import os
import time
import shutil
from sqlalchemy import event

BACKUP_DIR = "db_backups"
MAX_BACKUPS = 7

def create_backup(db_path):
    """
    Создает резервную копию базы данных.

    Если директория для резервных копий не существует, она будет создана. 
    Если количество резервных копий превышает MAX_BACKUPS, самая старая из них будет удалена. 
    Новая резервная копия будет создана с именем, содержащим текущую дату и время.

    Args:
        db_path (str): Путь к файлу базы данных, который нужно скопировать.
    """

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
    """
    Регистрирует обработчики событий для базы данных.

    Добавляет слушателя события 'before_commit' для SQLAlchemy, который создаёт резервную копию 
    базы данных перед каждым коммитом в сессии.

    Args:
        app: Flask приложение, содержащее конфигурацию и путь к базе данных.
        db: Объект базы данных SQLAlchemy.
    """
    
    @event.listens_for(db.session, "before_commit")
    def before_commit(session):
        db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
        if "sqlite:///:memory:" in db_uri:
            # База данных в памяти, резервную копию не делать
            return

        db_path = os.path.join(
            app.instance_path,
            db_uri.replace("sqlite:///", ""),
        )
        create_backup(db_path)