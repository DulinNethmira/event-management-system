from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.routes import events
from app.core.database import Base, engine
from app.models.user import User
from app.models.event import Event

app = FastAPI(
    title="EMS Backend",
    version="1.0.0",
    description="Event Management System API"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# Create upload directories
upload_dir = Path("uploads")
event_posters_dir = upload_dir / "event_posters"
event_posters_dir.mkdir(parents=True, exist_ok=True)

# Mount static files to serve uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Startup event - Create database tables
@app.on_event("startup")
def startup_event():
    print("=" * 50)
    print("🚀 Starting EMS Backend...")
    print("=" * 50)
    print("📦 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    print(f"📁 Upload directory: {event_posters_dir.absolute()}")
    print("=" * 50)

# Include routers
app.include_router(events.router)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to EMS API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "upload_directory": str(event_posters_dir.absolute())
    }