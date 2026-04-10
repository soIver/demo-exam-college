from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
import random

from state import state


class CaptchaException(Exception):
    def __init__(self, *args):
        self.type = "Ошибка при сборе капчи"
        super().__init__(*args)

class CaptchaTile(QLabel):
    image_size = 175

    def __init__(self, parent: "CaptchaPanel"):
        super().__init__()
        self.index = 0
        self.parent = parent
        self.setStyleSheet("""
            QLabel {
                border: 2px solid #ccc;
            }
            QLabel:focus {
                border: 2px solid #666;
            }
        """)
        self.setFixedSize(self.image_size, self.image_size)
        self.setFocusPolicy(Qt.TabFocus)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.index = (self.index + 1) % len(self.parent.image_fragments)
            self.update_image_fragment()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.index = (self.index + 1) % len(self.parent.image_fragments)
            self.update_image_fragment()
        super().keyPressEvent(event)

    def update_image_fragment(self):
        pixmap = self.parent.image_fragments[self.index]
        self.setPixmap(pixmap.scaled(self.image_size, self.image_size))


class CaptchaPanel(QWidget):
    _cols, _rows = 2, 2
    _total = _cols * _rows
    _right_order = list(range(_total))

    def __init__(self):
        super().__init__()
        self.image_fragments = []
        self.tiles = []
        
        grid = QGridLayout(self)
        self._load_images()
        
        for i in range(self._rows):
            for j in range(self._cols):
                tile = CaptchaTile(self)
                self.tiles.append(tile)
                grid.addWidget(tile, i, j)
        
        self.generate_captcha()

    def _load_images(self):
        path = os.path.join(os.path.dirname(__file__), '..', '..', 'source')
        for i in range(self._total):
            img_path = os.path.join(path, f'{i+1}.png')
            self.image_fragments.append(QPixmap(img_path))

    def generate_captcha(self):
        order = self._right_order.copy()
        while order == self._right_order:
            random.shuffle(order)
        for tile, idx in zip(self.tiles, order):
            tile.index = idx
            tile.update_image_fragment()

    def check(self):
        user_record = state.app_user.record(0)
        if not [tile.index for tile in self.tiles] == self._right_order:
            fail_auth_attempts = user_record.value("fail_auth_attempts")
            user_record.setValue("fail_auth_attempts", fail_auth_attempts+1)
            state.app_user.setRecord(0, user_record)
            state.app_user.submitAll()
            
            raise CaptchaException("Капча собрана неверно.")