from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.api.models.event import Event, EventStatus, Category, EventResponse
from app.api.core.database import get_db
router = APIRouter(prefix="/events", tags=["Events"])

# Request schema for creating/updating events
class EventCreate(BaseModel):
    title: str
    description: str
    category: Category
    status: EventStatus = EventStatus.DRAFT
    location: str
    starts_at: datetime
    ends_at: datetime
    capacity: int
    organizer_id: int

@router.post("/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(
        title=event.title,
        description=event.description,
        category=event.category,
        status=event.status,
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

@router.get("/", response_model=List[EventResponse])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, event_update: EventCreate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    for key, value in event_update.dict().items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}