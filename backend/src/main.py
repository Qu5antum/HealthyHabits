from fastapi import FastAPI, Request
from backend.src.database.db import init_models
from backend.src.security.security import *
from backend.src.services.user_service import *
from backend.src.services.reminder_service import *
from backend.src.models.schemas import *
from backend.src.dependencies.dependencies import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from backend.src.config.config import config
from backend.src.routes.habits_router import router as habit_router
from backend.src.routes.user_router import router as user_router
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

@app.post("/reminder/")
async def add_reminder(
    user_id: int,
    habit_id: int,
    reminder: RemindersCreate,
    session: AsyncSession = Depends(get_session)
):
    return await add_reminder_by_habit_id(
        session=session,
        user_id=user_id,
        habit_id=habit_id,
        reminder_name=reminder.name,
        reminder_time=reminder.time
    )               

@app.get("/reminder/")
async def get_reminder(
    habit_id: int,
    session: AsyncSession = Depends(get_session)
):
    result = await get_reminder_by_habit_id(session, habit_id)
    return result

if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run(
        "backend.src.main:app", host="127.0.0.1", port=8000, reload=True
)