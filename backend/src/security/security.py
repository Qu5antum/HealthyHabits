# будет создоваться jwt token хешировние дехешерование паролей, получение пользователя через token 
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from backend.src.config.config import config
from backend.src.database.db import get_session, AsyncSession
import jwt, datetime
from backend.src.security.security_context import *
from backend.src.models.schemas import UserCreate
from backend.src.models.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login/")

async def create_jwt_token(data):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

async def auth_user(credents: OAuth2PasswordRequestForm, session: AsyncSession = Depends(get_session)):
    query = select(User).where(User.username == credents.username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not check_hashes(credents.password, user.password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    token = await create_jwt_token({"sub": str(user.id)})
    return {"access_token": token}

async def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        playload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id: int = playload.get("sub")
        if user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token!")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="The token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")




        




    
