from components.main import MainWindow
from models.user import UserModel

class State():
    def __init__(self):
        self.app_window: MainWindow = None
        self.app_user: UserModel = None
        self.users: UserModel = None

state = State()