import asyncio
from app.api.core.database import SessionLocal
from app.api.utils.email import run_reminder_job


async def test():
    db = SessionLocal()
    print("Testing reminder system...")
    await run_reminder_job(db)
    db.close()
    print("Test complete!")


if __name__ == "__main__":
    asyncio.run(test())