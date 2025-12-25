from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    location: str = Field(..., min_length=1, max_length=255)
    start_time: datetime
    end_time: datetime
    capacity: int = Field(..., gt=0)
    price: float = Field(..., ge=0)


class EventCreate(EventBase):
    organizer_id: int


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    location: Optional[str] = Field(None, min_length=1, max_length=255)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    capacity: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, ge=0)


class EventResponse(EventBase):
    id: int
    organizer_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)