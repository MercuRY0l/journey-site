import pytest

from app.dto.login_dto import LoginDTO

from app.services.login_service import LoginService

from app.exceptions.login_exceptions import UserIsNotExists,  WrongPassword

from domain.models.auth_tokens_domain_model import AuthTokensDomainModel

from unittest.mock import Mock

from datetime import datetime, timezone

@pytest.fixture
def login_service():
    
    db_user_service = Mock()
    db_token_service = Mock()
    jwt_service = Mock()
    brute_service = Mock()
    hash_pass_service = Mock()
    hash_token_service = Mock()
    log_service = Mock()
    
    return LoginService(
        db_user_service=db_user_service,
        db_token_service=db_token_service,
        jwt_service=jwt_service,
        brute_service=brute_service,
        hash_pass_service=hash_pass_service,
        hash_token_service=hash_token_service,
        log_service=log_service
    )
    

def test_login_access(login_service):
    
    user = Mock()
    user.id = 1
    user.username = "example1"
    user.password = "123456"
    
    login_service.brute_service.is_blocked.return_value = False
    login_service.db_user_service.get_user_by_username.return_value = user
    login_service.hash_pass_service.check.return_value = True
    
    login_service.jwt_service.create_jwt_token.return_value = {
        "access" : "access_token",
        "refresh" : "refresh_token"
    }
    
    login_service.hash_token_service.hash.return_value = "hashed_refresh"
    
    dto = LoginDTO(username=user.username, password="hashed_pass", ip="127.0.0.1")
    
    result = login_service.login(log_dto=dto)
    
    assert result.access_token == "access_token"
    assert result.refresh_token == "refresh_token"
    
    login_service.brute_service.reset_attempts.assert_called_once()
    login_service.db_token_service.create_token.assert_called_once()
    
    
        
    created_token = login_service.db_token_service.create_token.call_args[0][0]
    
    assert created_token.user_id == user.id
    assert created_token.refresh_token == "hashed_refresh"
    assert created_token.expires_at > datetime.now(timezone.utc)
    
    
def test_login_user_not_exists(login_service):
    
    login_service.brute_service.is_blocked.return_value = False
    login_service.db_user_service.get_user_by_username.return_value = None
    login_service.brute_service.record_failed_attempt.return_value = 1
    
    dto = LoginDTO(username="unknown", password="123456", ip="127.0.0.1")
    
    with pytest.raises(UserIsNotExists):
        login_service.login(dto)
        
    login_service.brute_service.record_failed_attempt.assert_called_once()
    login_service.db_token_service.create_token.assert_not_called()



def test_login_wrong_password(login_service):
    user = Mock()
    user.password = "hashed_password"
    
    login_service.brute_service.is_blocked.return_value = False
    login_service.db_user_service.get_user_by_username.return_value = user
    login_service.hash_pass_service.check.return_value = False
    login_service.brute_service.record_failed_attempt.return_value = 2
    
    dto = LoginDTO(username="test_user", password="wrong_password", ip="127.0.0.1")
        
    with pytest.raises(WrongPassword):
        login_service.login(log_dto=dto)
    
    login_service.brute_service.record_failed_attempt.assert_called_once()
    

def test_login_blocked_by_brute(login_service):
    
    login_service.brute_service.is_blocked.return_value = True
    dto = LoginDTO(username="test_user", password="password", ip="127.0.0.1")
    
    with pytest.raises(ValueError, match="Слишком много попыток, попробуйте позже."):
        login_service.login(log_dto=dto)
        
    login_service.db_user_service.get_user_by_username.assert_not_called()
    