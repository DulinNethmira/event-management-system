from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, any_
from app.api.models.event import Event
from app.api.schemas.event_schema import EventCreate, EventUpdate
from typing import Optional, List
from datetime import datetime


def create_event(db: Session, event: EventCreate) -> Event:
    keywords_lower = [kw.lower().strip() for kw in event.keywords] if event.keywords else []
    
    db_event = Event(
        title=event.title,
        description=event.description,
        location=event.location,
        start_time=event.start_time,
        end_time=event.end_time,
        capacity=event.capacity,
        price=event.price,
        organizer_id=event.organizer_id,
        keywords=keywords_lower
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
    
    if "keywords" in update_data and update_data["keywords"] is not None:
        update_data["keywords"] = [kw.lower().strip() for kw in update_data["keywords"]]
    
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


def search_events(
    db: Session,
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 100
) -> list[Event]:
    query = db.query(Event)
    
    filters = []
    
    if keyword:
        keyword_lower = keyword.lower()
        keyword_filter = or_(
            Event.title.ilike(f"%{keyword}%"),
            Event.description.ilike(f"%{keyword}%"),
            Event.keywords.any(keyword_lower)
        )
        filters.append(keyword_filter)
    
    if location:
        filters.append(Event.location.ilike(f"%{location}%"))
    
    if start_date and end_date:
        date_filter = and_(
            Event.start_time >= start_date,
            Event.start_time <= end_date
        )
        filters.append(date_filter)
    elif start_date:
        filters.append(Event.start_time >= start_date)
    elif end_date:
        filters.append(Event.start_time <= end_date)
    
    if min_price is not None:
        filters.append(Event.price >= min_price)
    
    if max_price is not None:
        filters.append(Event.price <= max_price)
    
    if filters:
        query = query.filter(and_(*filters))
    
    return query.offset(skip).limit(limit).all()