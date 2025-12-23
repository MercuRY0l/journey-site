from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from presentation.routers.login_router import loginRouter
from presentation.routers.register_router import regRouter
from presentation.routers.other_routers import router
from presentation.routers.logout_router import logout_router
from presentation.routers.feedback_router import feedback_router
from presentation.routers.user_settings_router import user_setting_router

from infrastructure.database.init_db import init_db

init_db()

app = FastAPI()

origins = [
    
    "http://localhost:3000",
]

app.include_router(loginRouter)
app.include_router(regRouter)
app.include_router(router)
app.include_router(logout_router)
app.include_router(feedback_router)
app.include_router(user_setting_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

app.mount("/static", StaticFiles(directory="C:/Users/udgit/Documents/site_project_fastapi/frontend/static"), name = "static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host = "0.0.0.0", port=8000, reload=True)
    

    



    
    
    