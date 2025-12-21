from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class BookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"

class PaymentStatus(str, Enum):
    UNPAID = "UNPAID"
    PAID = "PAID"
    PARTIAL = "PARTIAL"
    REFUNDED = "REFUNDED"

class BookingBase(BaseModel):
    user_id: int
    event_id: int
    quantity: int
    amount_total: float
    currency: str = "LKR"

class BookingCreate(BookingBase):
    pass

class BookingRead(BookingBase):
    id: int
    status: BookingStatus
    payment_status: PaymentStatus
    booked_at: datetime

    class Config:
        orm_mode = True
