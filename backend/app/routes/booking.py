from fastapi import Depends, FastAPI, APIRouter
from sqlalchemy.orm import Session
from app.schemas.booking_schema import BookingCreate
from app.core.database import get_db

router = APIRouter(prefix="/bookings",tags=["Bookings"])

@router.get("/")
async def list_bookings():
    return {"message": "List of bookings"}

@router.post("/")
def create_booking(booking : BookingCreate, db:Session=Depends(get_db)):
    return create_booking(db, booking)
    
@router.get("/{booking_id}")
async def get_booking(booking_id: int):
    return {"message": f"Details of booking {booking_id}"}

@router.put("/{booking_id}")
async def update_booking(booking_id: int):
    return {"message": f"Booking {booking_id} updated"}

@router.delete("/{booking_id}")
async def delete_booking(booking_id: int):
    return {"message": f"Booking {booking_id} deleted"}

@router.get("/user/{user_id}")
async def list_user_bookings(user_id: int):
    return {"message": f"List of bookings for user {user_id}"}

@router.get("/event/{event_id}")
async def list_event_bookings(event_id: int):
    return {"message": f"List of bookings for event {event_id}"}

@router.post("/{booking_id}/cancel")
async def cancel_booking(booking_id: int):
    return {"message": f"Booking {booking_id} cancelled"}

@router.post("/{booking_id}/confirm")
async def confirm_booking(booking_id: int):
    return {"message": f"Booking {booking_id} confirmed"}


app = FastAPI()
app.include_router(router)