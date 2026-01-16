from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.core.database import get_db
from app.crud import event_crud
from app.schemas.event_schema import EventCreate, EventUpdate, EventResponse
from app.models import EventStatus, Category

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=EventResponse, status_code=201)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    return event_crud.create_event(db, event)

@router.get("/", response_model=List[EventResponse])
def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[EventStatus] = None,
    category: Optional[Category] = None,
    db: Session = Depends(get_db)):
    events = event_crud.get_events(db, skip, limit, status, category)
    return events

@router.get("/upcoming", response_model=List[EventResponse])
def get_upcoming_events(db: Session = Depends(get_db)):
    current_time = datetime.utcnow()
    events = event_crud.get_upcoming_events(db, current_time)
    return events

@router.get("/past", response_model=List[EventResponse])
def get_past_events(db: Session = Depends(get_db)):
    current_time = datetime.utcnow()
    events = event_crud.get_past_events(db, current_time)
    return events

@router.get("/search/location", response_model=List[EventResponse])
def search_events_by_location(
    location: str = Query(..., min_length=1),
    db: Session = Depends(get_db)):
    events = event_crud.get_events_by_location(db, location)
    return events

@router.get("/search/title", response_model=List[EventResponse])
def search_events_by_title(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db)):

    events = event_crud.get_events_by_title_keyword(db, keyword)
    return events

@router.get("/search/date-range", response_model=List[EventResponse])
def get_events_by_date_range(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    db: Session = Depends(get_db)):
    if start_date >= end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")
    
    events = event_crud.get_events_by_date_range(db, start_date, end_date)
    return events

@router.get("/search/capacity", response_model=List[EventResponse])
def get_events_by_capacity(
    min_capacity: int = Query(..., ge=0),
    max_capacity: int = Query(..., ge=1),
    db: Session = Depends(get_db)):
    if min_capacity > max_capacity:
        raise HTTPException(status_code=400, detail="min_capacity must be less than or equal to max_capacity")
    
    events = event_crud.get_events_by_capacity(db, min_capacity, max_capacity)
    return events

@router.get("/organizer/{organizer_id}", response_model=List[EventResponse])
def get_events_by_organizer(
    organizer_id: int,
    db: Session = Depends(get_db)):
    events = event_crud.get_events_by_organizer(db, organizer_id)
    return events

@router.get("/{event_id}", response_model=EventResponse)
def read_event(event_id: int, db: Session = Depends(get_db)):
    event = event_crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    updated_event: EventUpdate,
    db: Session = Depends(get_db)):
    event = event_crud.update_event(db, event_id, updated_event)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    success = event_crud.delete_event(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return "deleted successfully"