
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException


router = APIRouter()
templates = Jinja2Templates(directory="C:/Users/udgit/Documents/site_project_fastapi/frontend/static/html")


@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})

@router.get("/fishing")
async def root(request: Request):
    return templates.TemplateResponse("fishing_page.html", {"request" : request})

@router.get("/hunting")
async def root(request: Request):
    return templates.TemplateResponse("hunting_page.html", {"request" : request})

@router.get("/about")
async def root(request: Request):
    return templates.TemplateResponse("about_us.html", {"request" : request})

@router.get("/contacts")
async def root(request: Request):
    return templates.TemplateResponse("contacts_page.html", {"request" : request})

@router.get("/auth/me")
async def root(request: Request):
    token = request.cookies.get("refresh_token") or request.cookies.get("refresh")
    
    if not token:
        raise HTTPException(status_code=401)
    return {"status": "ok"}