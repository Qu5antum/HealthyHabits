from fastapi import APIRouter, status
from backend.src.security.security import *
from backend.src.services.user_service import *
from backend.src.models.schemas import *
from backend.src.database.db import get_session
from backend.src.dependencies.dependencies import get_current_user
from backend.src.config.config import config

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.post("/register/")
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await add_new_user(session, user)
   
@router.post("/login/")
async def login_user(credents: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await auth_user(credents, session)
    return user
    
