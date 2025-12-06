from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, time
from database.db import async_session
from backend.src.models.models import Reminder

# BETA !!!!!!!!!!!!!!!!!!
scheduler = AsyncIOScheduler()

async def check_reminders():
    async with async_session() as session:
        now = datetime.now().time().replace(second=0, microsecond=0)

        query = select(Reminder).where(Reminder.time == now)
        reminders = (await session.execute(query)).scalars().all()

        for r in reminders:
            print(f">>> Reminder for user={r.user_id} at {r.time}: {r.description}")
            # здесь можно отправить push/email/telegram/уведомления

def start_scheduler():
    scheduler.add_job(check_reminders, "cron", minute="*")  # проверять каждую минуту
    scheduler.start()