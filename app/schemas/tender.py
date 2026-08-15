from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import TenderStatus
from app.schemas.auth import UserRead


class TenderCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)


class TenderStatusUpdate(BaseModel):
    status: TenderStatus
    reason: str = Field(min_length=1, max_length=1000)


class TenderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None
    status: TenderStatus
    created_by: int
    created_at: datetime
    updated_at: datetime


class TenderStatusHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tender_id: int
    old_status: TenderStatus | None
    new_status: TenderStatus
    reason: str
    changed_by: int
    created_at: datetime
    changed_by_user: UserRead | None = None
