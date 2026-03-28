from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import QSqlDatabase
import sys

from components.main import MainWindow
from components.auth import AuthPanel
from components.captcha import CaptchaPanel
from components.workspace import Workspace
from utils.state import state
from config import config
from models.user import UserModel

app = QApplication(sys.argv)

# установление соединения с БД
db = QSqlDatabase.addDatabase('QPSQL')
db.setHostName(config.DB_HOST)
db.setPort(config.DB_PORT)
db.setDatabaseName(config.DB_NAME)
db.setUserName(config.DB_USER)
db.setPassword(config.DB_PASSWORD)
db.open()

# сохранение общих экземпляров в глобальном хранилище состояния state
state.app_window = MainWindow(auth=AuthPanel(), captcha=CaptchaPanel(), workspace=Workspace())
state.app_user = UserModel(db)
state.users = UserModel(db)

state.app_window.showMaximized()

sys.exit(app.exec_())