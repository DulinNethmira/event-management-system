"""
Booking Pydantic Schemas - Fixed Version
Complete request/response validation for booking operations
"""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from enum import Enum


# ============ ENUMS ============

class BookingStatus(str, Enum):
    """Booking status enumeration"""
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


class PaymentStatus(str, Enum):
    """Payment status enumeration"""
    UNPAID = "UNPAID"
    PAID = "PAID"
    PARTIAL = "PARTIAL"
    REFUNDED = "REFUNDED"


# ============ BASE SCHEMAS ============

class BookingBase(BaseModel):
    """Base schema - only fields that can be set during creation"""
    event_id: int = Field(..., gt=0, description="ID of the event to book")
    quantity: int = Field(..., gt=0, le=20, description="Number of tickets (1-20)")
    
    # Optional attendee information
    attendee_name: Optional[str] = Field(None, max_length=100, description="Attendee name")
    attendee_email: Optional[str] = Field(None, max_length=100, description="Attendee email")
    attendee_phone: Optional[str] = Field(None, max_length=20, description="Attendee phone")
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")
    
    @validator('quantity')
    def validate_quantity(cls, v):
        """Ensure quantity is positive"""
        if v <= 0:
            raise ValueError('Quantity must be greater than 0')
        if v > 20:
            raise ValueError('Cannot book more than 20 tickets at once')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "event_id": 1,
                "quantity": 2,
                "attendee_name": "John Doe",
                "attendee_email": "john@example.com",
                "attendee_phone": "+94771234567",
                "notes": "Vegetarian meal preference"
            }
        }


# ============ CREATE SCHEMA ============

class BookingCreate(BookingBase):
    """
    Schema for creating a new booking
    Note: user_id comes from authentication, not from request
    amount_total is calculated based on event price
    """
    pass


# ============ READ SCHEMA ============

class BookingRead(BaseModel):
    """
    Schema for reading booking data from database
    Includes all fields including system-generated ones
    """
    id: int = Field(..., description="Booking ID")
    user_id: int = Field(..., description="User who made the booking")
    event_id: int = Field(..., description="Booked event ID")
    quantity: int = Field(..., description="Number of tickets")
    amount_total: float = Field(..., description="Total amount")
    currency: str = Field(default="LKR", description="Currency code")
    status: BookingStatus = Field(default=BookingStatus.PENDING, description="Booking status")
    payment_status: PaymentStatus = Field(default=PaymentStatus.UNPAID, description="Payment status")
    booked_at: datetime = Field(..., description="Booking creation timestamp")
    
    # Optional fields
    attendee_name: Optional[str] = None
    attendee_email: Optional[str] = None
    attendee_phone: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        orm_mode = True  # For SQLAlchemy compatibility
        from_attributes = True  # Pydantic v2
        schema_extra = {
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
                "notes": "Window seat preferred"
            }
        }


# ============ UPDATE SCHEMA ============

class BookingUpdate(BaseModel):
    """
    Schema for updating booking
    All fields are optional - only update what's provided
    """
    quantity: Optional[int] = Field(None, gt=0, le=20, description="Update quantity")
    status: Optional[BookingStatus] = Field(None, description="Update booking status")
    payment_status: Optional[PaymentStatus] = Field(None, description="Update payment status")
    attendee_name: Optional[str] = Field(None, max_length=100)
    attendee_email: Optional[str] = Field(None, max_length=100)
    attendee_phone: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = Field(None, max_length=500)
    
    @validator('quantity')
    def validate_quantity(cls, v):
        """Validate quantity if provided"""
        if v is not None:
            if v <= 0:
                raise ValueError('Quantity must be greater than 0')
            if v > 20:
                raise ValueError('Cannot book more than 20 tickets at once')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "status": "CONFIRMED",
                "payment_status": "PAID"
            }
        }


# ============ ADDITIONAL RESPONSE SCHEMAS ============

class EventSummary(BaseModel):
    """Event summary for detailed booking response"""
    id: int
    title: str
    event_date: datetime
    venue_name: Optional[str] = None
    city: Optional[str] = None
    price: float
    currency: str = "LKR"
    
    class Config:
        orm_mode = True
        from_attributes = True


class UserSummary(BaseModel):
    """User summary for detailed booking response"""
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    
    class Config:
        orm_mode = True
        from_attributes = True


class BookingWithDetails(BookingRead):
    """
    Booking with full event and user details
    Use this for detailed API responses
    """
    event: Optional[EventSummary] = None
    user: Optional[UserSummary] = None
    
    class Config:
        orm_mode = True
        from_attributes = True


# ============ STATUS UPDATE SCHEMAS ============

class BookingStatusUpdate(BaseModel):
    """Schema for updating only booking status"""
    status: BookingStatus = Field(..., description="New booking status")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "CONFIRMED"
            }
        }


class PaymentStatusUpdate(BaseModel):
    """Schema for updating only payment status"""
    payment_status: PaymentStatus = Field(..., description="New payment status")
    
    class Config:
        schema_extra = {
            "example": {
                "payment_status": "PAID"
            }
        }


# ============ CANCELLATION SCHEMA ============

class BookingCancellation(BaseModel):
    reason: Optional[str] = Field(None, max_length=500, description="Cancellation reason")
    request_refund: bool = Field(default=False, description="Whether to request refund")
    
    class Config:
        schema_extra = {
            "example": {
                "reason": "Unable to attend",
                "request_refund": True
            }
        }


# ============ RESPONSE SCHEMAS ============

class BookingResponse(BaseModel):
    success: bool
    message: str
    booking: Optional[BookingRead] = None
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Booking created successfully",
                "booking": None
            }
        }


class BookingError(BaseModel):
    error: bool = True
    message: str
    error_code: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "error": True,
                "message": "Not enough seats available",
                "error_code": "INSUFFICIENT_SEATS"
            }
        }