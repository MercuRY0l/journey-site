

from infrastructure.repositories.user_repo import UserRepository
from infrastructure.services.jwt_tokens_service import JwtTokensService
from infrastructure.repositories.user_repo import UserRepository

from fastapi import Cookie
from fastapi.exceptions import HTTPException

async def get_current_user(
    access_token: str = Cookie(None),
):
    if not access_token:
        raise HTTPException(status_code=401)

    jwt_service = JwtTokensService()
    payload =  jwt_service.decode_jwt_token(access_token)

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401)

    repo = UserRepository()
    user = await repo.get_user_by_user_id(user_id=user_id)
    
    if not user:
        raise HTTPException(status_code=401)

    
    return user