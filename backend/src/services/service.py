from sqlalchemy import select
from fastapi import HTTPException, status
from backend.src.database.db import AsyncSession
from backend.src.models.models import User
from backend.src.models.schemas import UserCreate
from backend.src.security.security_context import hash_password

async def add_new_user(session: AsyncSession, usercreate: UserCreate):
    query = select(User).where(User.username == usercreate.username)
    result = await session.execute(query)
    exesting_user = result.scalar_one_or_none()

    if exesting_user: 
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User with this username already exist")
    
    new_user = User(
        username = usercreate.username,
        usergmail = usercreate.usergmail,
        password = hash_password(usercreate.password)
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user