


class TokenNotFound(ValueError):
    def __init__(self, msg = "Refresh токен не найден!"):
        super().__init__(msg)
        
        
class TokenTypeIncorrect(ValueError):
    def __init__(self, msg = "Неверный тип токена!"):
        super().__init__(msg)
        
class UserNotFound(ValueError):
    def __init__(self, msg = "Пользователь не найден!"):
        super().__init__(msg)
        
        
class TokenIsBlacklisted(ValueError):
     def __init__(self, msg = "Токен в черном списке!"):
        super().__init__(msg)