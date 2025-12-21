from __future__ import annotations
from datetime import datetime
from enum import Enum
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from models.ticket import Ticket
from models.event import Event
from models.wishlist import WishlistItem
from models.booking import Booking
from models.ticket import TicketComment

Base = declarative_base()


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    role: Mapped[UserRole] = mapped_column(String(20))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    events: Mapped[list["Event"]] = relationship("Event", back_populates="organizer", cascade="all, delete-orphan")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    wishlist_items: Mapped[list["WishlistItem"]] = relationship("WishlistItem", back_populates="user", cascade="all, delete-orphan")
    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="requester")
    assigned_tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="assignee")
    ticket_comments: Mapped[list["TicketComment"]] = relationship("TicketComment", back_populates="author")
