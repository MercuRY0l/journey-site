


class TokenNotFound(Exception):
    def __init__(self, msg = "Refresh токен не найден!"):
        super().__init__(msg)
        
        
class TokenTypeIncorrect(Exception):
    def __init__(self, msg = "Неверный тип токена!"):
        super().__init__(msg)
        
class UserNotFound(Exception):
    def __init__(self, msg = "Пользователь не найден!"):
        super().__init__(msg)
        
        
class TokenIsBlacklisted(Exception):
     def __init__(self, msg = "Токен в черном списке!"):
        super().__init__(msg)