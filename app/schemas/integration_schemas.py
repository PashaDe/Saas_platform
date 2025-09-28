from pydantic import BaseModel
from typing import Optional, Any


class ExportConfigCreate(BaseModel):
    entity_type: str
    target_spreadsheet_id: str
    target_sheet: str
    write_strategy: str = "replace"
    filters_json: Optional[Any] = None
    mapping_json: Optional[Any] = None
    schedule_cron: Optional[str] = None


class ExportConfigOut(BaseModel):
    id: str
    entity_type: str
    target_spreadsheet_id: str
    target_sheet: str
    write_strategy: str
    is_active: bool

    class Config:
        from_attributes = True


