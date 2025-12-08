from fastapi import APIRouter, status
from backend.src.security.security import *
from backend.src.services.habit_service import *
from backend.src.models.schemas import *
from backend.src.database.db import get_session
from backend.src.dependencies.dependencies import get_current_user

router = APIRouter(
    prefix="/habit",
    tags=["habits"]
)

@router.post("", status_code=status.HTTP_200_OK)
async def add_habits(
    habit: HealthyHabitCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await add_new_habit_by_user_id(
        session=session,
        user_id=user.id,
        title=habit.title,
        description=habit.description,
        goal=habit.goal
    )


@router.get("", status_code=status.HTTP_200_OK)
async def get_habits(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await get_habit_by_user_id(session, user.id)
    return result

@router.put("/{habit_id}", status_code=status.HTTP_200_OK)
async def update_habit(
    habit_id: int,
    habit: HealthyHabitCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await update_habit_by_user_id(
        session=session,
        user_id=user.id,
        habit_id=habit_id,
        title=habit.title,
        description=habit.description,
        goal=habit.goal
    )

@router.delete("/{habit_id}", status_code=status.HTTP_200_OK)
async def delete_habit(
    habit_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    await delete_habit_by_user_id(session, user.id, habit_id)
    return {"message": "Habit is deleted!"}