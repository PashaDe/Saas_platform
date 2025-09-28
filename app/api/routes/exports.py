from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.integration_schemas import ExportConfigCreate, ExportConfigOut
from app.models.integration_models import ExportConfig
from app.models.company_models import Company
from fastapi import HTTPException, status
from sqlalchemy import select
import uuid
from app.api.routes.auth import get_current_user, MeOut


router = APIRouter(prefix="/exports", tags=["exports"])


@router.get("/configs")
async def list_configs(current: MeOut = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(ExportConfig).where(ExportConfig.company_id == uuid.UUID(current.company_id)))
    items = [ExportConfigOut.model_validate(row) for row in result.scalars().all()]
    return {"items": items, "total": len(items)}

@router.post("/configs", response_model=ExportConfigOut)
async def create_config(payload: ExportConfigCreate, current: MeOut = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> ExportConfigOut:
    # Ensure company from token exists to avoid FK 500
    company_id = uuid.UUID(current.company_id)
    exists = await db.execute(select(Company.id).where(Company.id == company_id))
    if exists.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid company context. Re-login and try again.")
    config = ExportConfig(
        id=uuid.uuid4(),
        company_id=company_id,
        entity_type=payload.entity_type,
        filters_json=payload.filters_json,
        mapping_json=payload.mapping_json,
        target_spreadsheet_id=payload.target_spreadsheet_id,
        target_sheet=payload.target_sheet,
        write_strategy=payload.write_strategy,
        schedule_cron=payload.schedule_cron,
        is_active=True,
    )
    db.add(config)
    await db.commit()
    await db.refresh(config)
    return ExportConfigOut.model_validate(config)


