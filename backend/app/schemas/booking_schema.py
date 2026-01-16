from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
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
    event_id: int = Field(..., gt=0, description="ID of the event to book")
    quantity: int = Field(..., gt=0, le=20, description="Number of tickets (1-20)")

    attendee_name: Optional[str] = Field(None, max_length=100, description="Attendee name")
    attendee_email: Optional[str] = Field(None, max_length=100, description="Attendee email")
    attendee_phone: Optional[str] = Field(None, max_length=20, description="Attendee phone")
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")

    @validator("quantity")
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        if v > 20:
            raise ValueError("Cannot book more than 20 tickets at once")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_id": 1,
                "quantity": 2,
                "attendee_name": "John Doe",
                "attendee_email": "john@example.com",
                "attendee_phone": "+94771234567",
                "notes": "Vegetarian meal preference",
            }
        }
    }

class BookingCreate(BookingBase):
    pass

class BookingRead(BaseModel):
    id: int
    user_id: int
    event_id: int
    quantity: int
    amount_total: float
    currency: str = "LKR"
    status: BookingStatus = BookingStatus.PENDING
    payment_status: PaymentStatus = PaymentStatus.UNPAID
    booked_at: datetime

    attendee_name: Optional[str] = None
    attendee_email: Optional[str] = None
    attendee_phone: Optional[str] = None
    notes: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "user_id": 123,
                "event_id": 456,
                "quantity": 2,
                "amount_total": 5000.00,
                "currency": "LKR",
                "status": "CONFIRMED",
                "payment_status": "PAID",
                "booked_at": "2025-01-11T10:30:00",
                "attendee_name": "John Doe",
                "attendee_email": "john@example.com",
                "attendee_phone": "+94771234567",
                "notes": "Window seat preferred",
            }
        },
    }

class BookingUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0, le=20)
    status: Optional[BookingStatus] = None
    payment_status: Optional[PaymentStatus] = None
    attendee_name: Optional[str] = Field(None, max_length=100)
    attendee_email: Optional[str] = Field(None, max_length=100)
    attendee_phone: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = Field(None, max_length=500)

    @validator("quantity")
    def validate_quantity(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError("Quantity must be greater than 0")
            if v > 20:
                raise ValueError("Cannot book more than 20 tickets at once")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {"status": "CONFIRMED", "payment_status": "PAID"}
        }
    }

class EventSummary(BaseModel):
    id: int
    title: str
    event_date: datetime
    venue_name: Optional[str] = None
    city: Optional[str] = None
    price: float
    currency: str = "LKR"

    model_config = {"from_attributes": True}

class UserSummary(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None

    model_config = {"from_attributes": True}

class BookingWithDetails(BookingRead):
    event: Optional[EventSummary] = None
    user: Optional[UserSummary] = None

    model_config = {"from_attributes": True}

class BookingStatusUpdate(BaseModel):
    status: BookingStatus

    model_config = {
        "json_schema_extra": {"example": {"status": "CONFIRMED"}}
    }

class PaymentStatusUpdate(BaseModel):
    payment_status: PaymentStatus

    model_config = {
        "json_schema_extra": {"example": {"payment_status": "PAID"}}
    }

class BookingCancellation(BaseModel):
    reason: Optional[str] = Field(None, max_length=500)
    request_refund: bool = False

    model_config = {
        "json_schema_extra": {
            "example": {"reason": "Unable to attend", "request_refund": True}
        }
    }

class BookingResponse(BaseModel):
    success: bool
    message: str
    booking: Optional[BookingRead] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Booking created successfully",
                "booking": None,
            }
        }
    }

class BookingError(BaseModel):
    error: bool = True
    message: str
    error_code: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "error": True,
                "message": "Not enough seats available",
                "error_code": "INSUFFICIENT_SEATS",
            }
        }
    }