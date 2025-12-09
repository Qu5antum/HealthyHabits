from fastapi import APIRouter, status
from backend.src.security.security import *
from backend.src.services.ai_bot_service import add_message_responce_user_in_db, get_message_responce_user_in_db
from backend.src.models.schemas import *
from backend.src.database.db import get_session
from backend.src.dependencies.dependencies import get_current_user

router = APIRouter(
    prefix="/aibot",
    tags=["aibot"]
)

@router.post("", status_code=status.HTTP_200_OK)
async def ask_ai_bot(
    prompt: ChatBotMessageCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await add_message_responce_user_in_db(
        session=session,
        user_id=user.id,
        prompt=prompt.user_message
    )
    return {"answer": result}

@router.get("", status_code=status.HTTP_200_OK)
async def get_messages(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await get_message_responce_user_in_db(session, user.id)
    return result
    