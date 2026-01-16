from pydantic import BaseModel
from datetime import datetime

class WishlistItemCreate(BaseModel):
    user_id: int
    event_id: int

class WishlistItemRead(WishlistItemCreate):
    id: int
    added_at: datetime

    class Config:
        orm_mode = True
