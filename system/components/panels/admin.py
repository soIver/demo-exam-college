from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout

from components.views.users import UsersView
from state import state


class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        vlo = QVBoxLayout(self)
        
        self.users_view = UsersView()
        vlo.addWidget(self.users_view)

        controls_layout = QHBoxLayout()
        
        btn_del = QPushButton("Удалить")
        btn_del.clicked.connect(self.delete_user)
        
        btn_unblock = QPushButton("Разблокировать")
        btn_unblock.clicked.connect(self.unblock_user)

        btn_cancel = QPushButton("Отменить изменения")
        btn_cancel.clicked.connect(state.users.select)
        
        btn_add = QPushButton("Добавить")
        btn_add.clicked.connect(self.add_user)

        btn_save = QPushButton("Применить изменения")
        btn_save.clicked.connect(self.save_changes)

        controls_layout.addWidget(btn_del)
        controls_layout.addWidget(btn_unblock)
        controls_layout.addWidget(btn_cancel)
        controls_layout.addWidget(btn_add)
        controls_layout.addWidget(btn_save)
        
        vlo.addLayout(controls_layout)

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