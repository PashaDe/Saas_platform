from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db


router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("")
async def list_companies(db: AsyncSession = Depends(get_db)) -> dict:
    # TODO: query companies filtered by tenant/admin role
    return {"items": [], "total": 0}


@router.post("")
async def create_company(db: AsyncSession = Depends(get_db)) -> dict:
    # TODO: insert company
    return {"id": "placeholder"}


