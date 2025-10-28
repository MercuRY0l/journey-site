from fastapi import FastAPI
from sqlalchemy.orm import session


app = FastAPI()


@app.post('register/')
async def create_user(username):
    pass

@app.post('login/')
async def verify_user():
    pass

