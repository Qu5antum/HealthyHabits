from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import relationship
from backend.src.database.db import Base

#User modelin oluşumu
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    usergmail = Column(String, unique=True)
    password = Column(String)

    healthyhabit = relationship("HealthyHabit", back_populates="user", cascade="all, delete-orphan")
    chatbot = relationship("ChatBot", back_populates="user", cascade="all, delete-orphan")

#HealthyHabit modelin oluşumu
class HealthyHabit(Base):
    __tablename__ = "healtyhabits"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    goal = Column(String)
    reminders = Column(JSON)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="healthyhabit")

#ChatBot modelin oluşumu
class ChatBot(Base):
    __tablename__ = "chatbots"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    bot_answer = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="chatbot")

