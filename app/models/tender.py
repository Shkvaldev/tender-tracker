from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import TenderStatus
from app.models.user import User

_tender_status_enum = SAEnum(
    TenderStatus,
    native_enum=False,
    length=20,
    values_callable=lambda x: [e.value for e in x],
)


class Tender(Base):
    __tablename__ = "tenders"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TenderStatus] = mapped_column(
        _tender_status_enum, default=TenderStatus.DRAFT, index=True
    )
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class TenderStatusHistory(Base):
    __tablename__ = "tender_status_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    tender_id: Mapped[int] = mapped_column(
        ForeignKey("tenders.id", ondelete="CASCADE"), index=True
    )
    old_status: Mapped[Optional[TenderStatus]] = mapped_column(
        _tender_status_enum, nullable=True
    )
    new_status: Mapped[TenderStatus] = mapped_column(_tender_status_enum)
    reason: Mapped[str] = mapped_column(Text)
    changed_by: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    changed_by_user: Mapped[User] = relationship(User, lazy="raise")
