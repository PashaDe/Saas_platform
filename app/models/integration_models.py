import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import JSON

from .base import Base


class ProviderToken(Base):
    __tablename__ = "provider_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    provider = Column(String(32), nullable=False)  # google | moysklad
    account_ref = Column(String(255), nullable=True)
    credentials_json = Column(JSON, nullable=True)  # зашифрованные данные будут храниться как payload
    is_active = Column(Boolean, nullable=False, default=True)


class ExportConfig(Base):
    __tablename__ = "export_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    entity_type = Column(String(64), nullable=False)  # slug экспортёра
    filters_json = Column(JSON, nullable=True)
    mapping_json = Column(JSON, nullable=True)
    target_spreadsheet_id = Column(String(128), nullable=False)
    target_sheet = Column(String(128), nullable=False)
    write_strategy = Column(String(32), nullable=False, default="replace")  # append|upsert|replace
    schedule_cron = Column(String(64), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)


class ExportTask(Base):
    __tablename__ = "export_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    export_config_id = Column(UUID(as_uuid=True), ForeignKey("export_configs.id", ondelete="SET NULL"), nullable=True)
    status = Column(String(32), nullable=False, default="queued")
    idempotency_key = Column(String(128), nullable=True)
    error_summary = Column(String(1000), nullable=True)
    records_read = Column(String(32), nullable=True)
    records_written = Column(String(32), nullable=True)


