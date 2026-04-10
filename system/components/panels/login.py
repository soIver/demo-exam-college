from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QVBoxLayout

from state import state


class LoginException(Exception):
    def __init__(self, *args):
        self.type = "Ошибка авторизации"
        super().__init__(*args)

class LoginPanel(QWidget):
    def __init__(self):
        super().__init__()
        vlo = QVBoxLayout(self)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Логин")
        self.user_input.setMaxLength(32)
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Пароль")
        self.pass_input.setMaxLength(32)
        self.pass_input.setEchoMode(QLineEdit.Password)
        
        vlo.addWidget(QLabel("Учётные данные:"))
        vlo.addWidget(self.user_input)
        vlo.addWidget(self.pass_input)
        vlo.addStretch(1)

    def check(self):
        username = self.user_input.text()
        password = self.pass_input.text()

        if not (username and password):
            raise LoginException("Логин и пароль не могут быть пустыми.")
        
        user_record = state.app_user.select_by_field("username", username)
        fail_auth_attempts = user_record.value("fail_auth_attempts")

        if user_record.value("id") is None:
            raise LoginException("Вы ввели неверный логин или пароль. Пожалуйста, проверьте ещё раз введенные данные.")
        
        state.app_user.setRecord(0, user_record)
        if state.app_user.is_blocked():
            raise LoginException("Вы заблокированы. Обратитесь к администратору.")
        
        if user_record.value("password") != password:
            user_record.setValue("fail_auth_attempts", fail_auth_attempts+1)
            state.app_user.submitAll()
            
            raise LoginException("Вы ввели неверный логин или пароль. Пожалуйста, проверьте ещё раз введенные данные.")