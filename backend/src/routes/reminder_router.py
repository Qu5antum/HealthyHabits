from fastapi import APIRouter, status
from backend.src.security.security import *
from backend.src.services.reminder_service import *
from backend.src.models.schemas import *
from backend.src.database.db import get_session
from backend.src.dependencies.dependencies import get_current_user

router = APIRouter(
    prefix="/reminder",
    tags=["reminders"]
)

@router.post("")
async def add_reminder(
    habit_id: int,
    reminder: RemindersCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await add_reminder_by_habit_id(
        session=session,
        user_id=user.id,
        habit_id=habit_id,
        reminder_name=reminder.name,
        reminder_time=reminder.time
    )               

@router.get("")
async def get_reminder(
    habit_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await get_reminder_by_habit_id(session, user.id, habit_id)
    return result

@router.put("/{reminder_id}")
async def update_reminder(
    habit_id: int,
    reminder_id: int,
    reminder: RemindersCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await update_reminder_by_habit_id(
        session=session,
        user_id=user.id,
        habit_id=habit_id,
        reminder_id=reminder_id,
        reminder_name=reminder.name,
        reminder_time=reminder.time
    )

@router.delete("/{reminde_id}")
async def delete_reminder(
    habit_id: int,
    reminder_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    await delete_reminder_by_habit_id(session, user.id, habit_id, reminder_id)
    return {"message": "Reminder is deleted!"}


