from PyQt5.QtWidgets import QSizePolicy


EXPANDING_SIZE_POLICY = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

STYLESHEET = """

QMainWindow {
    background-color: #f2faff
}

QLabel {
    color: #333;
    font-size: 12pt;
}

QLabel#title {
    font-size: 20pt;
    font-weight: bold;
}

QLineEdit {
    background-color: #fff;
    border: 2px solid #ccc;
    border-radius: 15%;
    color: #333;
    font-size: 12pt;
    padding: 7px;
    margin: 0 10px 10px 10px;
}

QTableView {
    border: none;
    font-size: 12pt;
}

QTableView QLineEdit {
    border: none;
    border-radius: 0;
    padding: 0;
    margin: 0;
}

QPushButton {
    background-color: #7ec2f2;
    border: 2px solid #80a8c4;
    border-radius: 15%;
    color: #fff;
    font-size: 12pt;
    padding: 7px;
    margin: 10px;
}

QPushButton#danger {
    background-color: #f2867e;
    border: 2px solid #c48480;
}

QPushButton#confirm {
    background-color: #7ef291;
    border: 2px solid #80c48b;
}

QPushButton:hover {
    background-color: #96ccf4;
}

QPushButton#danger:hover {
    background-color: #f69c96;
}

QPushButton#confirm:hover {
    background-color: #96f7a5;
}

QPushButton:pressed, 
QPushButton#danger:pressed, 
QPushButton#confirm:pressed {
    border: none;
}

:focus, 
#danger:focus,
#confirm:focus {
    border-color: black;
}

QWidget#panel {
    background-color: #fff;
    border: 2px solid #ccc;
    border-radius: 20%;
}

"""