import os
import random
from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from utils.auth import check_captcha, AuthError, CaptchaError
from utils.state import state
from components.panel import AbstractPanel


class CaptchaTilesLayout(QGridLayout):
    _fragment_cols = 2
    _fragment_rows = 2
    _fragment_quantity = _fragment_cols * _fragment_rows
    _right_order = [i for i in range(_fragment_quantity)]

    def __init__(self):
        super().__init__()
        self.image_fragments: list[QPixmap] = []
        self.tiles: list[CaptchaTile] = []
        self.__load_image_fragments()

        for i in range(self._fragment_rows):
            for j in range(self._fragment_cols):
                new_tile = CaptchaTile(self)
                self.tiles.append(new_tile)
                self.addWidget(new_tile, i, j)

    def __load_image_fragments(self):
        images_path = "system/source/"

        for i in range(self._fragment_quantity):
            image_path = os.path.join(images_path, f"{i+1}.png")
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
            self.image_fragments.append(pixmap)

    def generate_captcha(self):
        shuffled_order = self._right_order.copy()
        while shuffled_order == self._right_order:
            random.shuffle(shuffled_order)
        for child, index in zip(self.tiles, shuffled_order):
            child.index = index
            child.update_image_fragment()

class CaptchaTile(QLabel):
    image_size = 175
    def __init__(self, parent_lo: CaptchaTilesLayout):
        super().__init__()
        self.index = 0
        self.parent_lo = parent_lo
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px solid #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QLabel:hover {
                border: 2px solid #4CAF50;
                background-color: #f0f0f0;
            }
            QLabel:focus {
                border: 2px solid #4CAF50;
                background-color: #e8f5e9;
            }
        """)
        self.setFixedSize(self.image_size, self.image_size)
        self.setFocusPolicy(Qt.TabFocus)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.index < len(self.parent_lo.image_fragments) - 1:
                self.index += 1
            else:
                self.index = 0
            self.update_image_fragment()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.index < len(self.parent_lo.image_fragments) - 1:
                self.index += 1
            else:
                self.index = 0
            self.update_image_fragment()
        return super().keyPressEvent(event)
    
    def update_image_fragment(self):
        self.setPixmap(self.parent_lo.image_fragments[self.index].scaled(self.image_size, self.image_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))

class CaptchaPanel(AbstractPanel):

    def __init__(self):
        super().__init__(
            "Капча", "Соберите исходную картинку, нажимая на фрагменты.",
            {"ver": 5, "hor": 10})

        main_widget_bottom_hlo = QHBoxLayout()
        main_widget_top_hlo = QHBoxLayout()

        back_button = QPushButton("Вернуться")
        back_button.setObjectName("danger")
        back_button.clicked.connect(lambda: state.app_window.update_and_set_active_page("auth"))

        check_captcha_button = QPushButton("Проверить")
        check_captcha_button.setObjectName("confirm")
        check_captcha_button.clicked.connect(self.__check_captha_button_action)
        self.captcha_lo = CaptchaTilesLayout()

        self.panel_widget_vlo.addStretch(1)
        self.panel_widget_vlo.addLayout(main_widget_top_hlo)
        self.panel_widget_vlo.addStretch(1)
        self.panel_widget_vlo.addLayout(main_widget_bottom_hlo)

        main_widget_top_hlo.addStretch(1)
        main_widget_top_hlo.addLayout(self.captcha_lo)
        main_widget_top_hlo.addStretch(1)

        main_widget_bottom_hlo.addWidget(back_button)
        main_widget_bottom_hlo.addWidget(check_captcha_button)

    def __check_captha_button_action(self):
        try:
            current_order = [tile.index for tile in self.captcha_lo.tiles]

            check_captcha(current_order, self.captcha_lo._right_order)
            QMessageBox.information(self, "Успех", "Вы успешно авторизовались.")

            state.app_window.update_and_set_active_page("workspace")

        except AuthError as e:
            QMessageBox.warning(self, e.type, *e.args)
            state.app_window.update_and_set_active_page("auth")

        except CaptchaError as e:
            QMessageBox.warning(self, e.type, *e.args)
            self.update()

        except Exception as e:
            import traceback
            QMessageBox.critical(self, "Ошибка", "Возникла непредвиденная ошибка.")
            print(traceback.format_exc())

    def update(self):
        self.captcha_lo.generate_captcha()
        return super().update()