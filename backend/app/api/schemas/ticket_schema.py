from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TicketStatusEnum(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TicketMessageCreate(BaseModel):
    message: str = Field(..., min_length=1)


class TicketMessageResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    message: str
    is_staff_reply: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class TicketCreate(BaseModel):
    subject: str = Field(..., min_length=3, max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    priority: TicketPriorityEnum = TicketPriorityEnum.MEDIUM
    message: str = Field(..., min_length=10)


class TicketUpdate(BaseModel):
    status: Optional[TicketStatusEnum] = None
    priority: Optional[TicketPriorityEnum] = None


class TicketResponse(BaseModel):
    id: int
    user_id: int
    subject: str
    category: Optional[str]
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TicketWithMessages(TicketResponse):
    messages: List[TicketMessageResponse] = []