from pydantic import BaseModel
from datetime import datetime
from enum import Enum

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

class EventBase(BaseModel):
    title: str
    description: str
    category: Category
    location: str
    starts_at: datetime
    ends_at: datetime
    capacity: int

class EventCreate(EventBase):
    organizer_id: int

class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: EventStatus | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    capacity: int | None = None

class EventRead(EventBase):
    id: int
    status: EventStatus
    organizer_id: int

    class Config:
        orm_mode = True
