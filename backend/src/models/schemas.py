from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Dict
from datetime import datetime
import string

# USER SCHEMAS
class UserCreate(BaseModel):
    username: str 
    usergmail: EmailStr
    password: str = Field(min_length=7, max_length=15, description="Şifre uzunluğu 7 ile 15 karakter arasında olmalıdır!")
    
    @field_validator("password")
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
        
        return password
    
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
    age: int = "Yaş (örn. 20)"
    sex: str = "Cinsiyet: Male / Female"
    smoke: str = "Sigara içme: Yes / No"
    
    weight: int = "Kilonuz (kg)"
    height: int = "Boyunuz (cm)"

    alcohol: str = "Alkol tüketimi: Yes / No"
    stroke: str = "Daha önce inme geçirdiniz mi?: Yes / No"

    physical_health: int = "Son 30 günde fiziksel sağlık problemleri yaşanan gün sayısı (0–30)"
    mental_health: int = "Son 30 günde mental sağlık problemleri yaşanan gün sayısı (0–30)"

    difficulty_walking: str = "Yürüyüş zorluğu var mı?: Yes / No"
    physical_activity: str = "Fiziksel aktivite düzeyi: Yes/No"

    general_health: str = "Genel sağlık durumu: poor / fair / good / very good / excellent"

    sleep: int = "Günde kaç saat uyuyorsunuz? (örn. 7)"
    
    high_sugar_level: str = "Hiç yüksek şeker seviyeniz oldu mu?: Yes / No (Diabetic)"
    asthma: str = "Astımınız var mı?: Yes / No"
    kidney_problems: str = "Böbrek sorunlarınız var mı?: Yes / No"
    skin_diseases: str = "Cilt hastalıklarınız var mı?: Yes / No"



