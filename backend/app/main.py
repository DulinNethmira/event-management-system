"""
FastAPI main entry point for Event Management System (ESMS)
Includes all routes and root health check
"""

from fastapi import FastAPI
from backend.app.api.routes import auth

app = FastAPI(title="Event Management System (ESMS)")

# Include all API routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint to verify that the backend is running
    """
    return {"message": "ESMS Backend Running"}
