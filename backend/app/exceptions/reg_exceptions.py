

class UserAlreadyExists(ValueError):
    def __init__(self, msg = "Пользователь уже существует!"):
        super().__init__(msg)
        
class EmailAlreadyExists(ValueError):
    def __init__(self, msg = "Email уже существует!"):
        super().__init__(msg)
        
class UsernameAlreadyExists(ValueError):
    def __init__(self, msg = "Логин уже существует!"):
        super().__init__(msg)
        
        
