from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Dict
from datetime import datetime
import string

# USER SCHEMAS
class UserCreate(BaseModel):
    username: str 
    usergmail: EmailStr
    password: str
    """Field(min_length=7, max_length=15, description="Şifre uzunluğu 7 ile 15 karakter arasında olmalıdır!")"""
    
    """@field_validator("password")
    def strong_password(cls, password):
        digits = string.digits
        lower_case = string.ascii_lowercase
        upper_case = string.ascii_uppercase
        punctuations = string.punctuation
    
        if not any(i in digits for i in password):
             raise ValueError("Şifrenizde en az bir rakam bulunmalıdır!")
        if not any(i in lower_case for i in password):
             raise ValueError("Şifrenizde en az bir küçük harf bulunmalıdır!")
        if not any(i in upper_case for i in password):
             raise ValueError("Şifrenizde en az bir büyük harf bulunmalıdır!")
        if not any(i in punctuations for i in password):
             raise ValueError("Şifrenizde en az bir özel karakter bulunmalıdır!")
        
        return password"""
    
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
    description: str | None = None
    goal: str

    class Config:
        from_attributes = True

# REMINDERS SCHEMAS
class RemindersCreate(BaseModel):
    name: str
    time: str 

    @field_validator("time")
    def validate_time(cls, value):
        try:
            datetime.strptime(value, "%H:%M")
        except ValueError:
            raise ValueError("Saat doğru formatınta değil. Örnek: 20:30")

        return value

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

from pydantic import BaseModel, Field

class HeartRiskInput(BaseModel):
    age: int 
    sex: str 
    smoke: str 
    
    weight: int 
    height: int

    alcohol: str
    stroke: str 

    physical_health: int 
    mental_health: int 

    difficulty_walking: str 
    physical_activity: str 

    general_health: str

    sleep: int 
    
    high_sugar_level: str 
    asthma: str 
    kidney_problems: str 
    skin_diseases: str 



