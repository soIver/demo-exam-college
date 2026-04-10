from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

from state import state
from components.panels.login import LoginPanel, LoginException
from components.panels.captcha import CaptchaPanel, CaptchaException


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()

        main_vlo = QVBoxLayout(self)
        
        title = QLabel("Авторизация")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")
        
        hint = QLabel("Введите логин, пароль и соберите капчу для входа.")
        hint.setAlignment(Qt.AlignCenter)
        
        # Левая часть: логин и пароль
        self.login = LoginPanel()
        
        # Правая часть: капча
        right_vlo = QVBoxLayout()
        right_vlo.addWidget(QLabel("Капча:"))
        self.captcha = CaptchaPanel()
        right_vlo.addWidget(self.captcha)
        right_vlo.addStretch(1)
        
        # Центральная часть: левая и правая части рядом
        content_hlo = QHBoxLayout()
        content_hlo.addStretch(1)
        content_hlo.addWidget(self.login, 1)
        content_hlo.addStretch(1)
        content_hlo.addWidget(self.captcha, 1)
        content_hlo.addStretch(1)
        
        btn = QPushButton("Войти")
        btn.setFixedWidth(200)
        btn.clicked.connect(self._auth)
        
        btn_hlo = QHBoxLayout()
        btn_hlo.addStretch(1)
        btn_hlo.addWidget(btn)
        btn_hlo.addStretch(1)
        
        main_vlo.addStretch(1)
        main_vlo.addWidget(title)
        main_vlo.addWidget(hint)
        main_vlo.addStretch(1)
        main_vlo.addLayout(content_hlo, 2)
        main_vlo.addStretch(1)
        main_vlo.addLayout(btn_hlo)
        main_vlo.addStretch(1)
    
    def _auth(self):
        try:
            self.login.check()
            self.captcha.check()
            QMessageBox.information(self, "Успех", "Вы успешно авторизовались.")
            state.app_window.set_active_page("workspace")
        
        except (LoginException, CaptchaException) as e:
            QMessageBox.warning(self, e.type, *e.args)
            self.update()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", "Непредвиденная ошибка.")
    
    def update(self):
        state.app_user.removeRow(0)
        self.login.user_input.clear()
        self.login.pass_input.clear()
        self.captcha.generate_captcha()