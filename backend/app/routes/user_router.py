from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate
from app.core.database import get_db
from app.crud.user_crud import create_user


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_users(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return {"message": f"Details of User {user_id}"}

app = FastAPI()
app.include_router(router)