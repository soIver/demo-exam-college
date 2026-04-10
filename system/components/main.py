from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget

class MainWindow(QMainWindow):
    def __init__(self, **pages: QWidget):
        super().__init__()
        self.setWindowTitle('Система молочного комбината "Полесье"')
        self.setMinimumSize(900, 600)

        self.stack = QStackedWidget()

        self.pages_indexes = {}
        for page_index, (page_name, page_obj) in enumerate(pages.items()):
            self.stack.addWidget(page_obj)
            self.pages_indexes[page_name] = page_index

        self.setCentralWidget(self.stack)

    def set_active_page(self, page_name: str):
        self.get_page_obj(page_name).update()
        self.stack.setCurrentIndex(self.pages_indexes.get(page_name))

    def get_page_obj(self, page_name: str):
        return self.stack.widget(self.pages_indexes.get(page_name))