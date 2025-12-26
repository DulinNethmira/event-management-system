from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.app.api.core.database import get_db
from backend.app.api.schemas.event_schema import EventCreate, EventUpdate, EventResponse
from backend.app.api.crud import event_crud
from typing import List, Optional
from datetime import datetime


router = APIRouter(tags=["Events"])


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    return event_crud.create_event(db=db, event=event)


@router.get("/", response_model=List[EventResponse])
def list_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return event_crud.get_events(db=db, skip=skip, limit=limit)


@router.get("/search", response_model=List[EventResponse])
def search_events(
    keyword: Optional[str] = Query(None, description="Search in title and description"),
    location: Optional[str] = Query(None, description="Filter by location"),
    start_date: Optional[datetime] = Query(None, description="Filter events from this date"),
    end_date: Optional[datetime] = Query(None, description="Filter events until this date"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return event_crud.search_events(
        db=db,
        keyword=keyword,
        location=location,
        start_date=start_date,
        end_date=end_date,
        min_price=min_price,
        max_price=max_price,
        skip=skip,
        limit=limit
    )


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    db_event = event_crud.get_event(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return db_event


@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, event_update: EventUpdate, db: Session = Depends(get_db)):
    db_event = event_crud.update_event(db=db, event_id=event_id, event_update=event_update)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return db_event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    success = event_crud.delete_event(db=db, event_id=event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return None