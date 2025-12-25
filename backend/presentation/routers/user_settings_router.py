

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

from app.services.settings_service import SettingsService
from app.dto.user_settings_dto import ChangeUsername, ChangeEmail, ChangePassword

from domain.services.log_service import LogService

from infrastructure.services.hash_pass_service import HashPassService
from infrastructure.services.brute_protection_service import BruteService

from infrastructure.repositories.user_repo import UserRepository
from infrastructure.repositories.log_repo import LogRepo

from presentation.routers.deps import get_current_user

user_setting_router = APIRouter()

templates = Jinja2Templates(directory="C:/Users/udgit/Documents/site_project_fastapi/frontend/static/html")


async def get_settings_service():
    
    user_repo = UserRepository()
    log_repo = LogRepo()
    
    return SettingsService(
        db_user_repo=user_repo,
        hash_pass_service=HashPassService(),
        log_service = LogService(log_repo),
        brute_service = BruteService()
    )


@user_setting_router.get("/user/settings") 
async def get(request: Request):
    return templates.TemplateResponse("user_settings_page.html", {'request' : request})

@user_setting_router.put("/user/settings/username")
async def update_username(
    data: ChangeUsername,
    user = Depends(get_current_user),
    service: SettingsService = Depends(get_settings_service)
):
    try:
        await service.change_username(data, user.id, data.new_username)
        return {"status": "success", "new_username": data.new_username}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_setting_router.put("/user/settings/email")
async def update_email(
    data: ChangeEmail,
    user = Depends(get_current_user),
    service: SettingsService = Depends(get_settings_service)
):
    try:
        await service.change_email(data, user.id, data.new_email)
        return {"status": "success", "new_email": data.new_email}
    
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_setting_router.put("/user/settings/password")
async def update_password(
    data: ChangePassword,
    user = Depends(get_current_user),
    service: SettingsService = Depends(get_settings_service)
):
    try:
        await service.change_password(data, user.id, data.new_password)
        return {"status": "success"}
    
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))