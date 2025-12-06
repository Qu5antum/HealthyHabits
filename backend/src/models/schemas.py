from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Dict
from datetime import datetime

# ДОБАВИТЬ ОГРАНИЧЕНИЕ В СХЕМАХ с field validator!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# USER SCHEMAS
class UserCreate(BaseModel):
    username: str
    usergmail: EmailStr
    password: str = Field(min_length=7, max_length=15, description="Şifre uzunluğu 7 ile 15 karakter arasında olmalıdır!")

class UserResponse(BaseModel):
    id: int
    username: str
    usergmail: EmailStr

    class Config:
        from_attributes = True

# HEALTHY HABIT SCHEMAS
class HealthyHabitCreate(BaseModel):
    title: str
    description: str | None = None
    goal: Optional[str] = Field(None, description="Sizin değer hedef")

class HealthyHabitResponse(BaseModel):
    id: int
    title: str
    description: str
    goal: str

    class Config:
        from_attributes = True

# REMINDERS SCHEMAS
class RemindersCreate(BaseModel):
    name: str | None = None
    time: str | None = None 

class RemindersResponce(BaseModel):
    id: int
    name: str
    time: str

# CHATBOT MESSAGE SCHEMAS
class ChatBotMessageCreate(BaseModel):
    user_message: str
    bot_answer: Optional[str] = None

class ChatBotMessageResponse(BaseModel):
    id: int
    user_message: str
    bot_answer: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True

# USER WITH RELATIONS
class UserFullResponse(BaseModel):
    id: int
    username: str
    usergmail: EmailStr
    healthyhabits: List[HealthyHabitResponse] = []
    chatbot_messages: List[ChatBotMessageResponse] = []

    class Config:
        from_attributes = True
