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
    ga_ticket_price: float | None = None
    vip_ticket_price: float | None = None
    pa_ticket_price: float | None = None

class EventCreate(EventBase):
    organizer_id: int
    status: EventStatus = EventStatus.DRAFT  
    

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

    model_config = {
        "from_attributes": True
    }

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    category: Category
    status: EventStatus
    location: str
    starts_at: datetime
    ends_at: datetime
    capacity: int
    organizer_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Tech Conference 2024",
                "description": "An annual conference focusing on the latest in technology.",
                "category": "CONFERENCE",
                "status": "PUBLISHED",
                "location": "San Francisco, CA",
                "starts_at": "2024-09-15T09:00:00",
                "ends_at": "2024-09-17T17:00:00",
                "capacity": 500,
                "organizer_id": 2,
                "created_at": "2024-06-01T12:00:00",
                "updated_at": "2024-06-10T15:30:00"
            }
        }
    }