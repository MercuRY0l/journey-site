

class UserAlreadyExists(Exception):
    def __init__(self, msg = "Пользователь уже существует!"):
        super().__init__(msg)
        
class EmailAlreadyExists(Exception):
    def __init__(self, msg = "Email уже существует!"):
        super().__init__(msg)
        
class UsernameAlreadyExists(Exception):
    def __init__(self, msg = "Логин уже существует!"):
        super().__init__(msg)
        
        
