from fastapi import FastAPI
from backend.app.api.routes import auth, events
from backend.app.api.core.database import engine, Base
from backend.app.api.models.user import User
from backend.app.api.models.event import Event


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management System (EMS)")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(events.router, prefix="/events", tags=["Events"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "EMS Backend Running"}