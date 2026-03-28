from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox, QGridLayout, QHBoxLayout

from utils.state import state
from components.panel import AbstractPanel
from components.users import UsersView

class Workspace(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.setLayout(self.grid)

    def clear_grid(self):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().deleteLater()

    def update(self):
        self.clear_grid()
        self.grid.addWidget(AccountPanel(), 0, 0)
        self.grid.setRowStretch(1, 20)
        if state.app_user.record(0).value("name") == "Администратор":
            self.grid.addWidget(AdminPanel(), 1, 0)
        return super().update()
        
class AccountPanel(AbstractPanel):
    def __init__(self):
        super().__init__(stretch_policy={"ver": 1, "hor": 1})
        username = state.app_user.record(0).value("username")
        role = state.app_user.record(0).value("name")
        login_label = QLabel(f"Вы авторизованы как {username} ({role})")
        logout_button = QPushButton("Выйти из аккаунта")
        logout_button.setObjectName("danger")
        logout_button.clicked.connect(lambda: state.app_window.update_and_set_active_page("auth"))
        main_widget_hlo = QHBoxLayout()
        main_widget_hlo.addWidget(login_label, 15)
        main_widget_hlo.addWidget(logout_button, 5)

        self.panel_widget_vlo.addLayout(main_widget_hlo)

class AdminPanel(AbstractPanel):
    def __init__(self):
        super().__init__(title_text="Пользователи", stretch_policy={"ver": 1, "hor": 1})
        
        self.users_view = UsersView()
        self.panel_widget_vlo.addWidget(self.users_view)

        controls_layout = QHBoxLayout()
        
        btn_del = QPushButton("Удалить")
        btn_del.setObjectName("danger")
        btn_del.clicked.connect(self.delete_user)
        
        btn_unblock = QPushButton("Разблокировать")
        btn_unblock.setObjectName("danger")
        btn_unblock.clicked.connect(self.unblock_user)

        btn_cancel = QPushButton("Отменить изменения")
        btn_cancel.setObjectName("danger")
        btn_cancel.clicked.connect(state.users.select)
        
        btn_add = QPushButton("Добавить")
        btn_add.clicked.connect(self.add_user)

        btn_save = QPushButton("Применить изменения")
        btn_save.setObjectName("confirm")
        btn_save.clicked.connect(self.save_changes)

        controls_layout.addWidget(btn_del)
        controls_layout.addWidget(btn_unblock)
        controls_layout.addWidget(btn_cancel)
        controls_layout.addWidget(btn_add)
        controls_layout.addWidget(btn_save)
        
        self.panel_widget_vlo.addLayout(controls_layout)

    def add_user(self):
        model = state.users
        row = model.rowCount()
        model.insertRow(row)
        
        idx = model.index(row, model.fieldIndex("fail_auth_attempts"))
        model.setData(idx, 0)
        idx = model.index(row, model.fieldIndex("name"))
        model.setData(idx, 1)
        
        self.users_view.scrollToBottom()
        self.users_view.selectRow(row)

    def delete_user(self):
        index = self.users_view.currentIndex()
        if not index.isValid():
            return
            
        row = index.row()
        target_id = state.users.record(row).value("id")
        current_id = state.app_user.record(0).value("id")

        if target_id == current_id:
            QMessageBox.warning(self, "Ошибка", "Вы не можете пометить на удаление собственный аккаунт.")
            return

        state.users.removeRow(row)

    def unblock_user(self):
        index = self.users_view.currentIndex()
        if not index.isValid():
            return
            
        col = state.users.fieldIndex("fail_auth_attempts")
        state.users.setData(state.users.index(index.row(), col), 0)

    def save_changes(self):
        if state.users.submitAll():
            state.users.select()
        else:
            error = state.users.lastError()
            error_text = error.text()
            if error.number() == 23505:
                username = error_text.split('=')[-1].split(')')[0].strip('(')
                error_text = f'Пользователь с логином "{username}" уже существует.'
            if error.number() == 23502:
                error_text = 'Не все обязательные поля заполнены.'

            QMessageBox.critical(
                self, "Транзакция отменена", error_text)