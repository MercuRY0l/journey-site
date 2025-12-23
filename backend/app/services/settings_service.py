

from infrastructure.repositories.user_repo import IUserRepository

class SettingsService:
    def __init__(self, db_user_repo : IUserRepository):
        self.db_user_repo = db_user_repo
    
    def change_username(self, username: str):
        pass
    
    def change_email(self, email: str):
        pass
    
    def change_password(self, password1 : str, password2 : str):
        pass
