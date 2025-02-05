from models.log import Log
from sqlalchemy.ext.asyncio import AsyncSession


async def log_event(session: AsyncSession, event: str, user_id: str = None, details: str = None):
    new_log = Log(event=event, user_id=user_id, details=details)
    session.add(new_log)
    await session.commit()
    await session.refresh(new_log)
