from fastapi import FastAPI
from routers import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

origins = [
    
    "http://localhost:3000",
]

app.include_router(router)
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
    

    



    
    
    