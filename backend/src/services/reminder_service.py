from sqlalchemy import select, update, delete
from fastapi import HTTPException, status
from backend.src.database.db import AsyncSession
from backend.src.models.models import HealthyHabit, Reminder, User
import datetime

# habit id ye göre yeni hatırlayıcı eklemek
async def add_reminder_by_habit_id(session: AsyncSession, user_id: int, habit_id: id, reminder_name: str = None, reminder_time: str = None):
    habit = await session.get(HealthyHabit, habit_id)
    if not habit:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Habit not founded!")
    
    if habit.user_id != user_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Habit not founded!")

    # ДОЛЖНО ВЫХИДИТЬ ОШИБКА ЕСЛИ ПОЛЬЗОВАТЕЛЬ ВВЕЛ НЕ ПОДХОДЯЩИЕ ЗНАЧЕНИЕ 
    hh, mm = map(int, reminder_time.split(":"))  
    
    new_reminder = Reminder(
        habit_id = habit.id,
        name = reminder_name,
        time = datetime.time(hh, mm)
    )

    session.add(new_reminder)
    await session.commit()
    await session.refresh(new_reminder)

    return new_reminder

# habit id ye göre yeni hatırlayıcı almak
async def get_reminder_by_habit_id(session: AsyncSession, user_id: int, habit_id: int):
    habit = await session.get(HealthyHabit, habit_id)
    if not habit:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Habit not founded!")
    
    if habit.user_id != user_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Habit not founded!")
    
    query = select(Reminder).where((HealthyHabit.id == habit_id) & (Reminder.habit_id == habit_id))
    result = await session.execute(query)
    return result.scalars().all()

# habit id göre hatırlayıcıyı güncellemek
async def update_reminder_by_habit_id(session: AsyncSession, user_id: int, habit_id: int, reminder_id: int, reminder_name: str = None, reminder_time: str = None):
    habit = await session.get(HealthyHabit, habit_id)
    if not habit:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Habit not founded!")
    
    if habit.user_id != user_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Habit not founded!")
    
    reminder = await session.get(Reminder, reminder_id)
    if not reminder:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Reminder not founded!")
    
    if reminder.habit_id != habit_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Reminder does not belong to this habit!")
    
    hh, mm = map(int, reminder_time.split(":")) 

    query = (
        update(Reminder)
        .where((Reminder.habit_id == habit_id) & (Reminder.id == reminder_id))
        .values(name = reminder_name, time=datetime.time(hh, mm))
        .returning(Reminder)
    )

    result = await session.execute(query)
    await session.commit()
    return result.scalar_one_or_none()

# habit id göre hatırlayıcıyı silmek
async def delete_reminder_by_habit_id(session: AsyncSession, user_id: int, habit_id: int, reminder_id: int):
    habit = await session.get(HealthyHabit, habit_id)
    if not habit:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Habit not founded!")
    
    if habit.user_id != user_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Habit not founded!")
    
    reminder = await session.get(Reminder, reminder_id)
    if not reminder:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Reminder not founded!")
    
    if reminder.habit_id != habit_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Reminder does not belong to this habit!")
    
    query = (delete(Reminder).where((Reminder.habit_id == habit_id) & (Reminder.id == reminder_id)))
    await session.execute(query)
    await session.commit()

