from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import events
from app.core.database import Base, engine
from app.models.user import User
from app.models.event import Event

app = FastAPI(
    title="EMS Backend",
    version="1.0.0",
    description="Event Management System API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5501",
        "http://localhost:5501",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8080",
        "http://localhost:8080",
        "*" ],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.on_event("startup")
def startup_event():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created!...................")
app.include_router(events.router)

@app.get("/")
def root():
    return {"message": "Welcome to EMS API", "version": "1.0.0"}