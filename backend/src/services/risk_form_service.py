from sqlalchemy import select, update, delete
from fastapi import HTTPException, status
from backend.src.database.db import AsyncSession
from backend.src.models.models import HeartRisk
from backend.src.models.schemas import HeartRiskInput

async def add_risk_form_by_user(
        session: AsyncSession,
        user_id: int,
        form: HeartRiskInput
): 
    new_form = HeartRisk(
        user_id = user_id,
        **form.model_dump()
    )

    session.add(new_form)
    await session.commit()
    await session.refresh(new_form)

    return new_form

async def get_form_from_user(session: AsyncSession, user_id: int):
    query = select(HeartRisk).where(HeartRisk.user_id == user_id)
    result = await session.execute(query)
    form = result.scalars().first()

    if not form: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Form is not founded!")
    
    return form


async def update_form_by_user(
        session: AsyncSession,
        user_id: int, 
        risk_form: HeartRiskInput,
):
    query = (
        update(HeartRisk)
        .where(HeartRisk.user_id == user_id)
        .values(**risk_form.model_dump())
        .returning(HeartRisk)
    )

    result = await session.execute(query)
    await session.commit()
    form = result.scalars().first()

    if not form: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Form is not founded!")
    
    return form
    
    
     