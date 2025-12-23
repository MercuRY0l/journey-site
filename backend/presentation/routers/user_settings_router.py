

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

user_setting_router = APIRouter()

templates = Jinja2Templates(directory="C:/Users/udgit/Documents/site_project_fastapi/frontend/static/html")




@user_setting_router.get("/user/settings") 
async def get(request: Request):
    return templates.TemplateResponse("user_settings_page.html", {'request' : request})


@user_setting_router.post("/user/settings/change_username")
async def post(request: Request):
    pass
    
    
    