import pytest
from unittest.mock import Mock
from datetime import datetime, timezone, timedelta

from app.services.logout_service import LogoutService
from app.dto.logout_dto import LogoutDTO
from app.exceptions.logout_exceptions import TokenNotFound
from domain.models.blacklist_domain_model import BlacklistDomainModel

@pytest.fixture
def logout_service():
    
    db_user_service=Mock()
    db_blacklisted_service = Mock()
    db_token_service=Mock()
    jwt_service = Mock()
    hash_token_service=Mock()
    log_service=Mock()
    brute_service=Mock()
    
    return LogoutService(
        db_user_service=db_user_service,
        db_blacklisted_service=db_blacklisted_service,
        db_token_service=db_token_service,
        jwt_service=jwt_service,
        hash_token_service=hash_token_service,
        log_service=log_service,
        brute_service=brute_service
        
        
        
    )

def test_logout_success(logout_service):
    refresh_token = "valid_refresh"
    
    logout_service.jwt_service.decode_jwt_token.return_value = {"user_id": 1, "type": "refresh"}
    
    user_in_db = Mock()
    user_in_db.id = 1
    user_in_db.username = "user1"
    logout_service.db_user_service.get_user_by_user_id.return_value = user_in_db
    
    logout_service.db_token_service.delete_refresh_token.return_value = 1
    logout_service.hash_token_service.hash.side_effect = lambda *args, **kwargs: f"hashed_{kwargs.get('token', args[0] if args else '')}"
    
    dto = LogoutDTO(refresh_token=refresh_token, ip="127.0.0.1")
    
    result = logout_service.logout(dto)
    
    assert result == {"status": "succses"}
    
    logout_service.db_token_service.delete_refresh_token.assert_called_once_with(
        user_id=user_in_db.id,
        hashed_token=f"hashed_{refresh_token}"
    )
    
    logout_service.db_blacklisted_service.create_blacklisted.assert_called_once()
    logout_service.log_service.create_log.assert_called()


def test_logout_no_token(logout_service):
    dto = LogoutDTO(refresh_token=None, ip="127.0.0.1")
    
    with pytest.raises(TokenNotFound):
        logout_service.logout(dto)
    
    logout_service.log_service.create_log.assert_called_once()


def test_logout_token_not_found(logout_service):
    refresh_token = "some_refresh"
    
    logout_service.jwt_service.decode_jwt_token.return_value = {"user_id": 1, "type": "refresh"}
    
    user_in_db = Mock()
    user_in_db.id = 1
    user_in_db.username = "user1"
    logout_service.db_user_service.get_user_by_user_id.return_value = user_in_db
    
    logout_service.db_token_service.delete_refresh_token.return_value = 0
    
    logout_service.hash_token_service.hash.side_effect = lambda x: f"hashed_{x}"
    
    dto = LogoutDTO(refresh_token=refresh_token, ip="127.0.0.1")
    
    with pytest.raises(TokenNotFound):
        logout_service.logout(dto)
    
    logout_service.log_service.create_log.assert_called()
