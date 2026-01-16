from sqlalchemy.orm import Session
from zstandard import backend
from ..models.booking import Booking
from ..schemas.booking_schema import BookingCreate


def create_booking(db: Session, booking: BookingCreate) -> Booking:
    new_booking =BookingCreate(
        event_id= BookingCreate.event_id,
        quantity= BookingCreate.quantity,
        attendee_name= BookingCreate.attendee_name,
        attendee_email=BookingCreate.attendee_email,
        attendee_phone= BookingCreate.attendee_phone,
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


def booking_read(db: Session, booking_id: int) -> Booking:
    return db.query(Booking).filter(Booking.id == booking_id).first()

def booking_update(db: Session, booking_id: int, update_data: dict) -> Booking:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    for key, value in update_data.items():
        setattr(booking, key, value)
    db.commit()
    db.refresh(booking)
    return booking

