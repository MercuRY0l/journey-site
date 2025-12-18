import pytest
from unittest.mock import Mock
from datetime import datetime, timezone, timedelta

from app.services.refresh_tokens_service import RefreshService
from app.dto.refresh_dto import RefreshDTO
from app.exceptions.refresh_exceptions import TokenNotFound, UserNotFound, TokenTypeIncorrect, TokenIsBlacklisted


@pytest.fixture
def refresh_service():
    
    db_blacklisted_service = Mock()
    db_user_service = Mock()
    db_token_service = Mock()
    jwt_service = Mock()
    brute_service = Mock()
    hash_token_service = Mock()
    log_service = Mock()
    
    
    return RefreshService(db_blacklisted_service=db_blacklisted_service, 
                          db_user_service=db_user_service, 
                          db_token_service=db_token_service,
                          jwt_service=jwt_service, 
                          hash_token_service=hash_token_service,
                          log_service=log_service, 
                          brute_service=brute_service)
    
    


def test_refresh_success(refresh_service):
    
    refresh_service.db_blacklisted_service.find_blacklisted_by_token.return_value = None
    
    payload = {"user_id": 1, "type": "refresh"}
    refresh_service.jwt_service.decode_jwt_token.return_value = payload
    
    user_from_db = Mock()
    user_from_db.id = 1
    user_from_db.username = "user1"
    refresh_service.db_user_service.get_user_by_user_id.return_value = user_from_db
    
    refresh_service.db_token_service.delete_refresh_token.return_value = 1
    
    refresh_service.jwt_service.create_jwt_token.return_value = {
        "access": "new_access",
        "refresh": "new_refresh"
    }
    
    refresh_service.hash_token_service.hash.side_effect = lambda x: f"hashed_{x}"
    
    dto = RefreshDTO(refresh_token="old_refresh", access_token="", ip="127.0.0.1")
    
    result = refresh_service.refresh(dto)
    
    assert result.refresh_token == "new_refresh"
    assert result.access_token == "new_access"
    assert result.ip == "127.0.0.1"
    
    
    refresh_service.db_token_service.create_token.assert_called_once()
    refresh_service.db_blacklisted_service.create_blacklisted.assert_called_once()
    refresh_service.log_service.create_log.assert_called()  # хотя бы один раз


def test_refresh_no_token(refresh_service):
    dto = RefreshDTO(refresh_token=None, access_token="", ip="127.0.0.1")
    
    with pytest.raises(ValueError):
        refresh_service.refresh(dto)
    
    refresh_service.log_service.create_log.assert_called_once()


def test_refresh_token_blacklisted(refresh_service):
    refresh_service.db_blacklisted_service.find_blacklisted_by_token.return_value = Mock()
    
    dto = RefreshDTO(refresh_token="some_refresh", access_token="", ip="127.0.0.1")
    
    with pytest.raises(TokenIsBlacklisted):
        refresh_service.refresh(dto)
    
    refresh_service.log_service.create_log.assert_called_once()


def test_refresh_user_not_found(refresh_service):
    payload = {"user_id": 99, "type": "refresh"}
    refresh_service.jwt_service.decode_jwt_token.return_value = payload

    refresh_service.db_user_service.get_user_by_user_id.return_value = None
    refresh_service.db_blacklisted_service.find_blacklisted_by_token.return_value = None
    
    dto = RefreshDTO(refresh_token="some_refresh", access_token="", ip="127.0.0.1")
    
    with pytest.raises(UserNotFound):
        refresh_service.refresh(dto)
    
    refresh_service.log_service.create_log.assert_called()

def test_refresh_token_type_incorrect(refresh_service):
    payload = {"user_id": 1, "type": "access"} 
    refresh_service.jwt_service.decode_jwt_token.return_value = payload
    
    user_from_db = Mock()
    user_from_db.id = 1
    user_from_db.username = "user1"
    refresh_service.db_user_service.get_user_by_user_id.return_value = user_from_db
    refresh_service.db_blacklisted_service.find_blacklisted_by_token.return_value = None
    
    dto = RefreshDTO(refresh_token="some_refresh", access_token="", ip="127.0.0.1")
    
    with pytest.raises(TokenTypeIncorrect):
        refresh_service.refresh(dto)
    
    refresh_service.log_service.create_log.assert_called()
