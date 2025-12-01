from fastapi import FastAPI
from app.api.routes import auth, events, booking, wishlist, support, admin

app = FastAPI(title="Event Management System")

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(booking.router)
app.include_router(wishlist.router)
app.include_router(support.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "ESMS Backend Running"}
