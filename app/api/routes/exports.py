from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db


router = APIRouter(prefix="/exports", tags=["exports"])


@router.get("/configs")
async def list_configs(db: AsyncSession = Depends(get_db)) -> dict:
    return {"items": [], "total": 0}

@router.post("/tasks")
async def create_task(db: AsyncSession = Depends(get_db)) -> dict:
    return {"task_id": "queued"}


