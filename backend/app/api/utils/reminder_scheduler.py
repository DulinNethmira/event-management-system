import asyncio
from datetime import datetime
from app.api.utils.email import run_reminder_job
from app.api.core.config import settings


async def schedule_reminder_job(db):
    while True:
        try:
            now = datetime.now()
            
            if now.hour == settings.REMINDER_TIME_HOUR and now.minute == 0:
                await run_reminder_job(db)
                await asyncio.sleep(60)
            
            await asyncio.sleep(60)
            
        except Exception as e:
            print(f"Scheduler Error: {e}")
            await asyncio.sleep(60)