import os
import httpx
from dotenv import load_dotenv

from fastapi import APIRouter
from fastapi import HTTPException, Request, status
from pydantic import BaseModel

load_dotenv()
BOT_TOKEN = os.getenv(key="BOT_TOKEN")
CHAT_ID = os.getenv(key="CHAT_ID")

feedback_router = APIRouter()
    

class FeedBackModel(BaseModel):
    name : str
    email : str
    message : str

@feedback_router.post("/feedback")
async def feedback(request: Request, data : FeedBackModel):
    
    refresh_token = request.cookies.get("refresh_token") or request.cookies.get("refresh")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    text_from_user = f"""
📩 Новое сообщение от пользователя
👤 Имя: {data.name}
✉️ Email: {data.email}
💬 Сообщение: {data.message}
"""
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        async with httpx.AsyncClient() as async_client:
            r = await async_client.post(url, json={
                "chat_id": CHAT_ID,
                "text": text_from_user
            })
            r.raise_for_status() 
            return {"status": "OK"}
    except httpx.HTTPStatusError as e:
        return {"status": "error", "detail": str(e)}