from PyQt5.QtWidgets import QWidget, QGridLayout

from state import state
from components.panels.account import AccountPanel
from components.panels.admin import AdminPanel

class WorkspaceWindow(QWidget):
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