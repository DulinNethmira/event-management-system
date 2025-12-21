from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import String, DateTime, Text, ForeignKey, Integer, Enum as SAEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .user import Base, User
from models.wishlist import WishlistItem
from models.booking import Booking

class EventStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class Category(str, Enum):
    CONFERENCE = "CONFERENCE"
    CONCERT = "CONCERT"
    WORKSHOP = "WORKSHOP"
    SPORTS = "SPORTS"
    MEETUP = "MEETUP"
    OTHER = "OTHER"

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[Category] = mapped_column(String(30))
    status: Mapped[EventStatus] = mapped_column(String(20), default=EventStatus.DRAFT.value)
    location: Mapped[str] = mapped_column(String(250))
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    capacity: Mapped[int] = mapped_column(Integer)  # total seats
    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    organizer: Mapped[User] = relationship("User", back_populates="events")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="event", cascade="all, delete-orphan")
    wishlist_items: Mapped[list["WishlistItem"]] = relationship("WishlistItem", back_populates="event", cascade="all, delete-orphan")
