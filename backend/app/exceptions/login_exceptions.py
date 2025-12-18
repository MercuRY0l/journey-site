


class UserIsNotExists(Exception):
    def __init__(self, msg = "Пользователя не существует или неверные данные!"):
        super().__init__(msg)
        
        
class WrongPassword(Exception):
    def __init__(self, msg = "Неверный пароль!"):
        super().__init__(msg)