

class UserNotFound(Exception):
    def __init__(self, msg = "Пользователь не найден!"):
        super().__init__(msg)
        
        
class EmailAlreadyExists(Exception):
    def __init__(self, msg = "Пользователь с такой почтой уже существует , введите другую почту!"):
        super().__init__(msg)
        
class UsernameAlreadyExists(Exception):
    def __init__(self, msg = "Пользователь с таким логином уже существует , введите другой логин!"):
        super().__init__(msg)
        