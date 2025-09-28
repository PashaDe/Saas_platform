from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.company_models import Company
from app.schemas.company_schemas import CompanyCreate, CompanyOut
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import uuid


router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("")
async def list_companies(db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(Company))
    items = [CompanyOut.model_validate(row) for row in result.scalars().all()]
    return {"items": items, "total": len(items)}


@router.post("", response_model=CompanyOut)
async def create_company(payload: CompanyCreate, db: AsyncSession = Depends(get_db)) -> CompanyOut:
    company = Company(
        id=uuid.uuid4(),
        name=payload.name,
        subdomain=payload.subdomain,
        plan_type=payload.plan_type,
    )
    db.add(company)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # Likely unique subdomain violation
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Company with this subdomain already exists",
        )
    await db.refresh(company)
    return CompanyOut.model_validate(company)


