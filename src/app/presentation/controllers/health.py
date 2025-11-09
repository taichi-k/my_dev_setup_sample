import logging

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.db.core import get_session

router = APIRouter()
log = logging.getLogger("app")


@router.get("/health")
async def health(session: AsyncSession = Depends(get_session)) -> dict:
    row = await session.execute(text("SELECT version()"))
    version = row.scalar_one()
    return {"ok": True, "db_version": version}
