from PyQt5.QtWidgets import QLineEdit, QTableView, QHeaderView, QStyledItemDelegate
from PyQt5.QtSql import QSqlRelationalDelegate
from PyQt5.QtCore import Qt
from utils.state import state


class EditorSizeDelegate(QSqlRelationalDelegate):
    def __init__(self, parent, max_size: int):
        super().__init__(parent)
        self.max_size = max_size

    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            editor.setMaxLength(self.max_size)
        return editor

class BlockedStatusDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return None
    
    def displayText(self, value, locale):
        try:
            return "Да" if int(value) >= 3 else "Нет"
        except (ValueError, TypeError):
            return str(value)

class UsersView(QTableView):
    def __init__(self):
        super().__init__()
        self.users_model = state.users
        self.users_model.select()
        self.setModel(self.users_model)
        self.sortByColumn(0, Qt.AscendingOrder)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.hideColumn(0)

        # выпадающий список для ролей
        self.setItemDelegate(QSqlRelationalDelegate(self))

        # ограничение на размер полей логина и пароля
        username_idx = self.users_model.fieldIndex("username")
        self.setItemDelegateForColumn(username_idx, EditorSizeDelegate(self, 32))
        password_idx = self.users_model.fieldIndex("password")
        self.setItemDelegateForColumn(password_idx, EditorSizeDelegate(self, 32))

        # отображение статуса блокировки в зависимости от количества попыток авторизации
        fail_idx = self.users_model.fieldIndex("fail_auth_attempts")
        self.setItemDelegateForColumn(fail_idx, BlockedStatusDelegate(self))

        headers = {
            "id": "ID", 
            "username": "Логин", 
            "password": "Пароль", 
            "name": "Роль", 
            "fail_auth_attempts": "Заблокирован"
        }
        for i in range(self.users_model.columnCount()):
            field = self.users_model.record().fieldName(i)
            if field in headers:
                self.users_model.setHeaderData(i, Qt.Horizontal, headers[field])