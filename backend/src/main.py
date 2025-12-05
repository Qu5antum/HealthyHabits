from fastapi import FastAPI, Request
from backend.src.database.db import init_models
from backend.src.security.security import *
from backend.src.services.service import add_new_user
import asyncio
import uvicorn

app = FastAPI()

@app.post("/register/")
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await add_new_user(session, user)

@app.post("/login/")
async def login_user(credents: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await auth_user(session, credents)
    return user

if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run(
        "backend.src.main:app", host="127.0.0.1", port=8000, reload=True
)