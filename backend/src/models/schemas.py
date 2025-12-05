from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime



# USER SCHEMAS
class UserCreate(BaseModel):
    username: str
    usergmail: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    usergmail: EmailStr

    class Config:
        from_attributes = True



# HEALTHY HABIT SCHEMAS
class HealthyHabitCreate(BaseModel):
    title: str
    description: str
    goal: str
    reminders: List[str] = []   # JSON list


class HealthyHabitResponse(BaseModel):
    id: int
    title: str
    description: str
    goal: str
    reminders: List[str]

    class Config:
        from_attributes = True



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
