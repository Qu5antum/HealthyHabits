from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, JSON, Time
from sqlalchemy.orm import relationship
from backend.src.database.db import Base

#User modelin oluşumu
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) #по возмозности добавить uuid
    username = Column(String, unique=True)
    usergmail = Column(String, unique=True)
    password = Column(String)

    healthyhabit = relationship("HealthyHabit", back_populates="user", cascade="all, delete-orphan")
    chatbot = relationship("ChatBot", back_populates="user", cascade="all, delete-orphan")

#HealthyHabit modelin oluşumu
class HealthyHabit(Base):
    __tablename__ = "healthyhabits"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    goal = Column(String, nullable=True)
    
    reminder = relationship("Reminder", back_populates="habit", cascade="all, delete-orphan")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="healthyhabit")

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    time = Column(Time)

    habit_id = Column(Integer, ForeignKey("healthyhabits.id"))
    habit = relationship("HealthyHabit", back_populates="reminder")

#ChatBot modelin oluşumu
class ChatBot(Base):
    __tablename__ = "chatbots"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    bot_answer = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="chatbot")

