from sqlalchemy.orm import Session
from backend.app.api.models.event import Event
from backend.app.api.schemas.event_schema import EventCreate, EventUpdate
from typing import Optional


def create_event(db: Session, event: EventCreate) -> Event:
    db_event = Event(
        title=event.title,
        description=event.description,
        location=event.location,
        start_time=event.start_time,
        end_time=event.end_time,
        capacity=event.capacity,
        price=event.price,
        organizer_id=event.organizer_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event(db: Session, event_id: int) -> Optional[Event]:
    return db.query(Event).filter(Event.id == event_id).first()


def get_events(db: Session, skip: int = 0, limit: int = 100) -> list[Event]:
    return db.query(Event).offset(skip).limit(limit).all()


def update_event(db: Session, event_id: int, event_update: EventUpdate) -> Optional[Event]:
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        return None
    
    update_data = event_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int) -> bool:
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        return False
    
    db.delete(db_event)
    db.commit()
    return True