from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from app.api.routes import auth, events, support
from app.api.core.database import engine, Base, SessionLocal
from app.api.models.user import User
from app.api.models.event import Event
from app.api.utils.reminder_scheduler import schedule_reminder_job


Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    task = asyncio.create_task(schedule_reminder_job(db))
    print("Email reminder scheduler started")
    
    yield
    
    task.cancel()
    db.close()
    print("Email reminder scheduler stopped")


app = FastAPI(
    title="Event Management System (EMS)",
    lifespan=lifespan
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(support.router, prefix="/support", tags=["Support Tickets"])


@app.get("/", tags=["Root"])
def root():
    return {"message": "EMS Backend Running"}