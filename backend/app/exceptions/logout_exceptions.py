


class TokenNotFound(ValueError):
    def __init__(self, msg = "Refresh токен не найден!"):
        super().__init__(msg)