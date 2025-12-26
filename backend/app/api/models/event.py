from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, ARRAY
from sqlalchemy.sql import func
from backend.app.api.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    keywords = Column(ARRAY(String), nullable=True, default=[])
    created_at = Column(DateTime, server_default=func.now(), nullable=False)