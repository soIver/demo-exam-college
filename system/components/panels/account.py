from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox, QGridLayout, QHBoxLayout, QVBoxLayout

from state import state


class AccountPanel(QWidget):
    def __init__(self):
        super().__init__()
        vlo = QVBoxLayout(self)
        username = state.app_user.record(0).value("username")
        role = state.app_user.record(0).value("name")
        login_label = QLabel(f"Вы авторизованы как {username} ({role})")
        logout_button = QPushButton("Выйти из аккаунта")
        logout_button.setObjectName("danger")
        logout_button.clicked.connect(lambda: state.app_window.set_active_page("auth"))
        main_widget_hlo = QHBoxLayout()
        main_widget_hlo.addWidget(login_label, 15)
        main_widget_hlo.addWidget(logout_button, 5)
        vlo.addLayout(main_widget_hlo)
        vlo.addStretch(1)