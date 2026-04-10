import dotenv
import os

dotenv.load_dotenv()

class Config():
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    STYLESHEET = """
        QWidget#panel { border: 1px solid black; }
        QLabel { font-size: 14pt; }
        QLabel#title { font-size: 16pt; font-weight: bold; }
        QLineEdit, QPushButton { font-size: 12pt; border: 1px solid black; padding: 5px; }
        QMessageBox { font-size: 14pt; }
    """

config = Config()