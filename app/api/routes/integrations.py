from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db


router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("/status")
async def integrations_status(db: AsyncSession = Depends(get_db)) -> dict:
    return {"google": {"connected": False}, "moysklad": {"connected": False}}

@router.post("/google/connect")
async def google_connect(db: AsyncSession = Depends(get_db)) -> dict:
    return {"ok": True}


