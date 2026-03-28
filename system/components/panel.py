from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout

from styles.main import EXPANDING_SIZE_POLICY


class AbstractPanel(QWidget):
    def __init__(self, title_text: str = None, hint_text: str = None, stretch_policy: dict[str, int] = {}):
        super().__init__()

        panel_hlo = QHBoxLayout(self)
        panel_vlo = QVBoxLayout()
        panel_widget = QWidget()

        panel_widget.setObjectName("panel")
        panel_widget.setSizePolicy(EXPANDING_SIZE_POLICY)
        self.setSizePolicy(EXPANDING_SIZE_POLICY)

        self.panel_widget_vlo = QVBoxLayout(panel_widget)

        if hint_text:
            hint_label = QLabel(hint_text)
            hint_label.setContentsMargins(10, 0, 0, 0)
            self.panel_widget_vlo.addWidget(hint_label)

        panel_vlo.addStretch(stretch_policy.get("ver", 1))

        if title_text:
            title_label = QLabel(title_text)
            title_label.setObjectName("title")
            panel_vlo.addWidget(title_label, 1)

        panel_vlo.addWidget(panel_widget, 20)
        panel_vlo.addStretch(stretch_policy.get("ver", 1))

        panel_hlo.addStretch(stretch_policy.get("hor", 1))
        panel_hlo.addLayout(panel_vlo, 20)
        panel_hlo.addStretch(stretch_policy.get("hor", 1))