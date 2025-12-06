from fastapi import FastAPI, Request
from backend.src.database.db import init_models
from backend.src.security.security import *
from backend.src.services.user_service import *
from backend.src.services.habit_service import *
from backend.src.services.reminder_service import *
from backend.src.models.schemas import *
import asyncio
import uvicorn

app = FastAPI()

@app.post("/register/")
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        return await add_new_user(session, user)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Not registered!")
   
@app.post("/login/")
async def login_user(credents: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    try:
        user = await auth_user(session, credents)
        return user
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not logined")

@app.post("/user/{user_id}/habit")
async def add_habits(
    user_id: int,
    habit: HealthyHabitCreate,
    session: AsyncSession = Depends(get_session)
):
    try:
        return await add_new_habit_by_user_id(
            session=session,
            user_id=user_id,
            title=habit.title,
            description=habit.description,
            goal=habit.goal
        )
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Habit not added!")

@app.get("/user/{user_id}/habit")
async def get_habits(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    try:
        result = await get_habit_by_user_id(session, user_id)
        return result
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error!")

@app.put("/user/{user_id}/habit")
async def update_habit(
    user_id: int,
    habit_id: int,
    habit: HealthyHabitCreate,
    session: AsyncSession = Depends(get_session)
):
    try:
        return await update_habit_by_user_id(
            session=session,
            user_id=user_id,
            habit_id=habit_id,
            title=habit.title,
            description=habit.description,
            goal=habit.goal
        )
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Habits not updated")

@app.delete("/user/{user_id}/habit")
async def delete_habit(
    user_id: int,
    habit_id: int,
    session: AsyncSession = Depends(get_session)
):
    try:
        await delete_habit_by_user_id(session, user_id, habit_id)
        return {"message": "Habit is deleted!"}
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Habits not deleted!")

@app.post("/user/{user_id}/habit/{habit_id}/reminder")
async def add_reminder(
    user_id: int,
    habit_id: int,
    reminder: RemindersCreate,
    session: AsyncSession = Depends(get_session)
):
    try:
        return await add_reminder_by_habit_id(
            session=session,
            user_id=user_id,
            habit_id=habit_id,
            reminder_name=reminder.name,
            reminder_time=reminder.time
        )               
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Reminder is not added!")

@app.get("/user/{user_id}/habit/{habit_id}/reminder")
async def get_reminder(
    habit_id: int,
    session: AsyncSession = Depends(get_session)
):
    try:
        result = await get_reminder_by_habit_id(session, habit_id)
        return result
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error!")

if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run(
        "backend.src.main:app", host="127.0.0.1", port=8000, reload=True
)