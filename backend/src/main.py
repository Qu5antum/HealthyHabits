from fastapi import FastAPI
from backend.src.database.db import init_models
from fastapi.middleware.cors import CORSMiddleware
from backend.src.config.config import config
from backend.src.routes.habits_router import router as habit_router
from backend.src.routes.user_router import router as user_router
from backend.src.routes.reminder_router import router as reminder_router
from backend.src.routes.ai_bot_router import router as ai_router
import asyncio
import uvicorn

app = FastAPI(
    title = config.app_name,
    debug=config.debug,
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = config.cors_origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(user_router)
app.include_router(habit_router)
app.include_router(reminder_router)
app.include_router(ai_router)


if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run(
        "backend.src.main:app", host="127.0.0.1", port=8000, reload=True
)