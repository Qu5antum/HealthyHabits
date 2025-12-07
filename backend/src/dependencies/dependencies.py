from fastapi import Depends, HTTPException, status
from backend.src.database.db import get_session, AsyncSession
from backend.src.models.models import User
from backend.src.security.security import get_user_from_token

async def get_current_user(user_id: int = Depends(get_user_from_token), session: AsyncSession = Depends(get_session)):
    user = await session.get(User, int(user_id))
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not founded!")
    return user

