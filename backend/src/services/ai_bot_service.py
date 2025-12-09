from sqlalchemy import select, update, delete
from fastapi import HTTPException, status
from backend.src.chat_bot.ai_bot import ai_response
from backend.src.database.db import AsyncSession
from backend.src.models.models import User, HealthyHabit, ChatBot

async def get_goal_by_user_id(session: AsyncSession, user_id: int):
     query = select(HealthyHabit.goal).where(HealthyHabit.user_id == user_id)
     result = await session.execute(query)
     goals = result.scalars().all()

     return goals if goals else None

async def add_message_responce_user_in_db(session: AsyncSession, user_id: int, prompt: str):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not founded!")
    
    bad_answer = [
        "Bu konu sağlıklı alışkanlıklarla ilgili görünmüyor. Bu konuda yardımcı olabilirim",
        "Tam olarak anlayamadım, biraz daha ayrıntı verebilir misin?"
    ]
    
    bot_answer = await ai_response(prompt)

    goals = await get_goal_by_user_id(session=session, user_id=user.id)
    
    goals_and_prompt = prompt + " benim hedeflerim: " + str(goals)

    if bot_answer not in bad_answer:
        new_message = ChatBot(
            user_message = goals_and_prompt,
            bot_answer = bot_answer,
            user_id=user.id
        )

        session.add(new_message)
        await session.commit()
        await session.refresh(new_message)

    return bot_answer

async def get_message_responce_user_in_db(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not founded!")
    
    query = (
        select(ChatBot)
        .where(ChatBot.user_id == user_id)
    )

    result = await session.execute(query)
    return result.scalars().all()


