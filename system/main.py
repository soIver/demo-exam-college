from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import QSqlDatabase
import sys

from components.main import MainWindow
from components.pages.auth import AuthWindow
from components.pages.workspace import WorkspaceWindow
from state import state
from config import config
from models.user import UserModel

app = QApplication(sys.argv)

STYLESHEET = """
    QWidget#panel { border: 1px solid black; }
    QLabel { font-size: 14pt; }
    QLabel#title { font-size: 16pt; font-weight: bold; }
    QLineEdit, QPushButton { font-size: 12pt; border: 1px solid black; padding: 5px; }
    QMessageBox { font-size: 14pt; }
"""
app.setStyleSheet(STYLESHEET)

# установление соединения с БД
db = QSqlDatabase.addDatabase('QPSQL')
db.setHostName(config.DB_HOST)
db.setPort(config.DB_PORT)
db.setDatabaseName(config.DB_NAME)
db.setUserName(config.DB_USER)
db.setPassword(config.DB_PASSWORD)
db.open()

# сохранение общих экземпляров в глобальном хранилище состояния state
state.app_window = MainWindow(auth=AuthWindow(), workspace=WorkspaceWindow())
state.app_user = UserModel(db)
state.users = UserModel(db)

state.app_window.showNormal()

sys.exit(app.exec_())