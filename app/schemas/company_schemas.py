from pydantic import BaseModel
from typing import Optional


class CompanyCreate(BaseModel):
    name: str
    subdomain: Optional[str] = None
    plan_type: Optional[str] = None


class CompanyOut(BaseModel):
    id: str
    name: str
    subdomain: Optional[str] = None
    plan_type: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


