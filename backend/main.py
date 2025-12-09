from fastapi import FastAPI
from presentation.routers.login_router import LoginRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

origins = [
    
    "http://localhost:3000",
]

login_router = LoginRouter()


app.include_router(login_router)
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
    

    



    
    
    