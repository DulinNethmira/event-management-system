from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import Event, EventStatus, Category
from app.schemas.event_schema import EventCreate, EventUpdate

def create_event(db: Session, event: EventCreate) -> Event:
    db_event = Event(
        title=event.title,
        description=event.description,
        category=event.category,
        status=event.status or EventStatus.DRAFT.value,
        location=event.location,
        starts_at=event.starts_at,
        ends_at=event.ends_at,
        capacity=event.capacity,
        organizer_id=event.organizer_id,
        
    )
    db.add(db_event)
    db.commit() 
    db.refresh(db_event)
    return db_event

def list_events(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
    return db.query(Event).offset(skip).limit(limit).all()

def get_event(db: Session, event_id: int) -> Optional[Event]:
    return db.query(Event).filter(Event.id == event_id).first()

def get_events(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    status: Optional[EventStatus] = None,
    category: Optional[Category] = None
) -> List[Event]:
    query = db.query(Event)
    
    if status:
        query = query.filter(Event.status == status.value)
    
    if category:
        query = query.filter(Event.category == category.value)
    
    return query.offset(skip).limit(limit).all()

def update_event(db: Session, event_id: int, updated_event: EventUpdate) -> Optional[Event]:
    db_event = get_event(db, event_id)
    if not db_event:
        return None
    
    for var, value in vars(updated_event).items():
        if value is not None:
            setattr(db_event, var, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int) -> bool:
    db_event = get_event(db, event_id)
    if not db_event:
        return False
    
    db.delete(db_event)
    db.commit()
    return True

def get_events_by_organizer(db: Session, organizer_id: int) -> List[Event]:
    return db.query(Event).filter(Event.organizer_id == organizer_id).all()

def get_upcoming_events(db: Session, current_time) -> List[Event]:
    return db.query(Event).filter(Event.starts_at > current_time).all()

def get_past_events(db: Session, current_time) -> List[Event]:
    return db.query(Event).filter(Event.ends_at < current_time).all()

def get_events_by_location(db: Session, location: str) -> List[Event]:
    return db.query(Event).filter(Event.location.ilike(f"%{location}%")).all()

def get_events_by_date_range(db: Session, start_date, end_date) -> List[Event]:
    return db.query(Event).filter(Event.starts_at >= start_date, Event.ends_at <= end_date).all()

def get_events_by_capacity(db: Session, min_capacity: int, max_capacity: int) -> List[Event]:
    return db.query(Event).filter(Event.capacity >= min_capacity, Event.capacity <= max_capacity).all()

def get_events_by_title_keyword(db: Session, keyword: str) -> List[Event]:
    return db.query(Event).filter(Event.title.ilike(f"%{keyword}%")).all()

