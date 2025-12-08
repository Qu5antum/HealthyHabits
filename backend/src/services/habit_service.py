from sqlalchemy import select, update, delete
from fastapi import HTTPException, status
from backend.src.database.db import AsyncSession
from backend.src.models.models import User, HealthyHabit
from backend.src.models.schemas import HealthyHabitCreate, HealthyHabitResponse, UserCreate, UserResponse

# kulanıcı id ye göre yeni habit eklemek 
async def add_new_habit_by_user_id(session: AsyncSession, user_id: int, title: str, description: str = None, goal: str = None):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not founded!") # возможно надо убрать
    
    new_habit = HealthyHabit(
        user_id=user_id,
        title=title,
        description=description,
        goal=goal
    )

    session.add(new_habit)
    await session.commit()
    await session.refresh(new_habit)

    return new_habit

# kulanıcı id ye göre habit almak
async def get_habit_by_user_id(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not founded!")
    
    query = select(HealthyHabit).where(HealthyHabit.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()

# kullanıcı id ye göre habit değiştirmek
async def update_habit_by_user_id(session: AsyncSession, user_id: int, habit_id: int, title: str = None, description: str = None, goal: str = None):
    habit = await session.get(HealthyHabit, habit_id)
    if not habit:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Habit not founded!")
    
    if habit.user_id != user_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Habit not founded!")
    
    query = (
        update(HealthyHabit)
        .where((HealthyHabit.id == habit_id) & (HealthyHabit.user_id == user_id))
        .values(title=title, description=description, goal=goal)
        .returning(HealthyHabit)
    )

    result = await session.execute(query)
    await session.commit()
    return result.scalar_one_or_none()

# user id ye göre habiti silmek
async def delete_habit_by_user_id(session: AsyncSession, user_id: int, habit_id: int):
    habit = await session.get(HealthyHabit, habit_id)
    if not habit:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Habit not founded!")
    
    if habit.user_id != user_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Habit not founded!")
    
    query = delete(HealthyHabit).where((HealthyHabit.id == habit_id) & (HealthyHabit.user_id == user_id))
    await session.execute(query)
    await session.commit()