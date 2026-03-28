from utils.state import state
from PyQt5.QtSql import QSqlRecord
from models.user import UserModel

class AuthError(Exception):
    def __init__(self, *args):
        self.type = "Ошибка авторизации"
        super().__init__(*args)

class CaptchaError(Exception):
    def __init__(self, *args):
        self.type = "Ошибка в капче"
        super().__init__(*args)

def check_credentails(username: str, password: str):
        if not (username and password):
            raise AuthError("Логин и пароль не могут быть пустыми.")
        
        user_record = state.app_user.select_by_field("username", username)
        fail_auth_attempts = user_record.value("fail_auth_attempts")

        if user_record.value("id") is None:
            raise AuthError("Вы ввели неверный логин или пароль. Пожалуйста, проверьте ещё раз введенные данные.")
        
        if state.app_user.is_blocked():
            raise AuthError("Вы заблокированы. Обратитесь к администратору.")
        if user_record.value("password") != password:
            user_record.setValue("fail_auth_attempts", fail_auth_attempts+1)
            state.app_user.setRecord(0, user_record)
            state.app_user.submitAll()
            if state.app_user.is_blocked():
                raise AuthError("Вы заблокированы. Обратитесь к администратору.")
            raise AuthError("Вы ввели неверный логин или пароль. Пожалуйста, проверьте ещё раз введенные данные.")
        
        user_record.setValue("fail_auth_attempts", 0)
        state.app_user.setRecord(0, user_record)
        state.app_user.submitAll()

def check_captcha(current_order: list[int], right_order: list[int]):
    user_record = state.app_user.record(0)
    if current_order == right_order:
        user_record.setValue("fail_auth_attempts", 0)
        
    else:
        fail_auth_attempts = user_record.value("fail_auth_attempts")
        user_record.setValue("fail_auth_attempts", fail_auth_attempts+1)
        state.app_user.setRecord(0, user_record)
        state.app_user.submitAll()
        if state.app_user.is_blocked():
            raise AuthError("Вы заблокированы. Обратитесь к администратору.")
        raise CaptchaError("Капча собрана неверно.")