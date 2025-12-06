from sqlalchemy import select
from fastapi import HTTPException, status
from backend.src.database.db import AsyncSession
from backend.src.models.models import HealthyHabit, Reminder, User
from backend.src.models.schemas import RemindersCreate, RemindersResponce, HealthyHabitResponse, UserResponse
import datetime

# ПЕРЕПИсАТЬ КОД ДОБАВИТЬ ПОИСК ПО USER_ID!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# habit id ye göre yeni hatırlayıcı eklemek
async def add_reminder_by_habit_id(session: AsyncSession, user_id: UserResponse, habit_id: HealthyHabitResponse, reminder_name: RemindersCreate, reminder_time: RemindersCreate):
    habit = await session.get(HealthyHabit, habit_id)
    if not habit or habit.user_id != user_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Habit not founded for this user!")
    
    hh, mm = map(int, reminder_time.split(":"))  
    
    new_reminder = Reminder(
        habit_id = habit_id,
        name = reminder_name,
        time = datetime.time(hh, mm)
    )

    session.add(new_reminder)
    await session.commit()
    await session.refresh(new_reminder)

    return new_reminder

# habit id ye göre yeni hatırlayıcı almak
async def get_reminder_by_habit_id(session: AsyncSession, habit_id: HealthyHabitResponse):
    habit = await session.get(HealthyHabit, habit_id)
    if not habit:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Habit not founded!")
    
    query = select(Reminder).where(Reminder.habit_id == habit_id)
    result = await session.execute(query)
    return result.scalars().all()
