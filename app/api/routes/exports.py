from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.integration_schemas import ExportConfigCreate, ExportConfigOut
from app.models.integration_models import ExportConfig
from sqlalchemy import select
import uuid


router = APIRouter(prefix="/exports", tags=["exports"])


@router.get("/configs")
async def list_configs(db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(ExportConfig))
    items = [ExportConfigOut.model_validate(row) for row in result.scalars().all()]
    return {"items": items, "total": len(items)}

@router.post("/configs", response_model=ExportConfigOut)
async def create_config(payload: ExportConfigCreate, db: AsyncSession = Depends(get_db)) -> ExportConfigOut:
    config = ExportConfig(
        id=uuid.uuid4(),
        company_id=uuid.uuid4(),  # TODO: replace with tenant company_id
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


