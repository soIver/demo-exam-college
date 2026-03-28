from PyQt5.QtWidgets import QLineEdit, QPushButton, QMessageBox

from utils.auth import AuthError, check_credentails
from utils.state import state
from components.panel import AbstractPanel


class AuthPanel(AbstractPanel):
    def __init__(self):
        super().__init__(
            "Авторизация", "Введите логин и пароль для входа в систему.",
            {"ver": 20, "hor": 15})
       
        self.username_le = QLineEdit()
        self.username_le.setPlaceholderText("Логин")
        self.username_le.setMaxLength(32)

        self.password_le = QLineEdit()
        self.password_le.setPlaceholderText("Пароль")
        self.password_le.setMaxLength(32)
        self.password_le.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Войти")
        
        login_button.clicked.connect(self.__login_button_action)  

        self.panel_widget_vlo.addWidget(self.username_le)
        self.panel_widget_vlo.addWidget(self.password_le)
        self.panel_widget_vlo.addWidget(login_button)

    def __login_button_action(self):
        try:
            username = self.username_le.text()
            password = self.password_le.text()

            check_credentails(username, password)

            state.app_window.update_and_set_active_page("captcha")

        except AuthError as e:
            QMessageBox.warning(self, e.type, *e.args)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", "Возникла непредвиденная ошибка.")
            print(e)

    def update(self):
        self.username_le.clear()
        self.password_le.clear()
        return super().update()
    