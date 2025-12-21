from __future__ import annotations
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .user import Base, User
from .event import Event

class WishlistItem(Base):
    __tablename__ = "wishlist_items"
    __table_args__ = (
        UniqueConstraint("user_id", "event_id", name="uq_wishlist_user_event"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), index=True)
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship("User", back_populates="wishlist_items")
    event: Mapped[Event] = relationship("Event", back_populates="wishlist_items")
