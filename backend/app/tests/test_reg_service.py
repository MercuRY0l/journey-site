import pytest

from app.dto.register_dto import RegisterDTO

from app.services.register_service import RegisterService

from app.exceptions.reg_exceptions import UserAlreadyExists,  UsernameAlreadyExists, EmailAlreadyExists

from unittest.mock import Mock

from datetime import datetime, timezone

@pytest.fixture
def reg_service():
    
    
    db_user_service = Mock()
    db_token_service = Mock()
    jwt_service = Mock()
    brute_service = Mock()
    hash_pass_service = Mock()
    hash_token_service = Mock()
    log_service = Mock()
    
    
    return RegisterService(
        db_user_service=db_user_service,
        db_token_service=db_token_service,
        jwt_service=jwt_service,
        brute_service=brute_service,
        hash_pass_service=hash_pass_service,
        hash_token_service=hash_token_service,
        log_service=log_service
    )
    

def test_reg_access(reg_service):
    
    user = Mock()
    user.username = "example_random"
    user.password = "123456"
    user.email = "random_mail@mail.ru"
        
    reg_service.brute_service.is_blocked.return_value = False
    reg_service.db_user_service.get_user_by_username.return_value = None
    reg_service.db_user_service.get_user_by_email.return_value = None
    reg_service.db_user_service.get_user_by_user_id.return_value = None
    
    reg_service.brute_service.record_failed_attempt.return_value = 0
    
    reg_service.jwt_service.create_jwt_token.return_value = {
        "access" : "access_token",
        "refresh" : "refresh_token"
    }
    
    reg_service.hash_token_service.hash.return_value = "hashed_refresh"
    
    
    created_user = Mock()
    created_user.username = user.username
    created_user.password = "hashed_pass"
    created_user.email = user.email
    reg_service.db_user_service.create_user.return_value = created_user
    
    
    dto = RegisterDTO(username=created_user.username, password=created_user.password, email=created_user.email ,ip="127.0.0.1")
    result = reg_service.register(reg_dto=dto)
    
    assert result.access_token == "access_token"
    assert result.refresh_token == "refresh_token"
    
    reg_service.brute_service.reset_attempts.assert_called_once()
    reg_service.db_token_service.create_token.assert_called_once()
    
    created_token = reg_service.db_token_service.create_token.call_args[0][0]
    
    assert created_token.user_id == created_user.id
    assert created_token.refresh_token == "hashed_refresh"
    assert created_token.expires_at > datetime.now(timezone.utc)
    
    
def test_reg_username_already_exists(reg_service):
    
    user_in_db = Mock()
    user_in_db.username = "user1"
    user_in_db.password = "123456"
    user_in_db.email = "user_email1@mail.ru"
    
    reg_service.brute_service.is_blocked.return_value = False
    
    reg_service.db_user_service.get_user_by_username.return_value = user_in_db
    reg_service.db_user_service.get_user_by_email.return_value = None
    
    reg_service.brute_service.record_failed_attempt.return_value = 1
    
    dto = RegisterDTO(username="user1", password="123456", email=user_in_db.email, ip="127.0.0.1")
    
    with pytest.raises(UserAlreadyExists):
        reg_service.register(dto)
        
    reg_service.brute_service.record_failed_attempt.assert_called_once()
    reg_service.db_token_service.create_token.assert_not_called()



def test_reg_email_already_exists(reg_service):
    
    user_in_db = Mock()
    user_in_db.username = "user1"
    user_in_db.password = "123456"
    user_in_db.email = "user_email1@mail.ru"
    
    reg_service.brute_service.is_blocked.return_value = False
    
    reg_service.db_user_service.get_user_by_username.return_value = None
    reg_service.db_user_service.get_user_by_email.return_value = user_in_db
    
    reg_service.brute_service.record_failed_attempt.return_value = 1
    
    dto = RegisterDTO(username="user1", password="123456", email=user_in_db.email, ip="127.0.0.1")
    
    with pytest.raises(UserAlreadyExists):
        reg_service.register(dto)
        
    reg_service.brute_service.record_failed_attempt.assert_called_once()
    reg_service.db_token_service.create_token.assert_not_called()


    

def test_reg_blocked_by_brute(reg_service):
    
    reg_service.brute_service.is_blocked.return_value = True
    dto = RegisterDTO(username="test_user", password="password", email="test_email@mail.ru" ,ip="127.0.0.1")
    
    with pytest.raises(ValueError, match="Слишком много попыток, попробуйте позже."):
        reg_service.register(reg_dto=dto)
        
    reg_service.db_user_service.get_user_by_username.assert_not_called()
    