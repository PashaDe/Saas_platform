import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    subdomain = Column(String(255), nullable=True, unique=True)
    plan_type = Column(String(50), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)


