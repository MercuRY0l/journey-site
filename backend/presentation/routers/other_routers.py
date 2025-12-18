
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request



router = APIRouter()
templates = Jinja2Templates(directory="C:/Users/udgit/Documents/site_project_fastapi/frontend/static/html")


@router.get("/")
def root(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})

@router.get("/fishing")
def root(request: Request):
    return templates.TemplateResponse("fishing_page.html", {"request" : request})

@router.get("/hunting")
def root(request: Request):
    return templates.TemplateResponse("hunting_page.html", {"request" : request})

@router.get("/about")
def root(request: Request):
    return templates.TemplateResponse("about_us.html", {"request" : request})

@router.get("/contacts")
def root(request: Request):
    return templates.TemplateResponse("contacts_page.html", {"request" : request})