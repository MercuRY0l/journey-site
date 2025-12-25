


class UserIsNotExists(ValueError):
    def __init__(self, msg = "Пользователя не существует или неверные данные!"):
        super().__init__(msg)
        
        
class WrongPassword(ValueError):
    def __init__(self, msg = "Неверный пароль!"):
        super().__init__(msg)