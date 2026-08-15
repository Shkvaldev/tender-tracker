from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.config import settings
from app.models import Tender, TenderStatus, TenderStatusHistory, User
from app.schemas.tender import TenderCreate, TenderStatusUpdate


async def _get_tender_or_404(db: AsyncSession, tender_id: int) -> Tender:
    tender = await db.scalar(select(Tender).where(Tender.id == tender_id))
    if tender is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tender not found")
    return tender


async def create_tender(db: AsyncSession, payload: TenderCreate, current_user: User) -> Tender:
    tender = Tender(
        title=payload.title,
        description=payload.description,
        status=TenderStatus.DRAFT,
        created_by=current_user.id,
    )
    db.add(tender)
    await db.flush()

    history = TenderStatusHistory(
        tender_id=tender.id,
        old_status=None,
        new_status=TenderStatus.DRAFT,
        reason="Тендер создан",
        changed_by=current_user.id,
    )
    db.add(history)
    await db.commit()
    await db.refresh(tender)
    return tender


async def update_tender_status(
    db: AsyncSession, tender_id: int, payload: TenderStatusUpdate, current_user: User
) -> Tender:
    tender = await _get_tender_or_404(db, tender_id)
    old_status = tender.status
    new_status = payload.status

    if old_status == new_status:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Статус уже установлен")

    tender.status = new_status
    history = TenderStatusHistory(
        tender_id=tender.id,
        old_status=old_status,
        new_status=new_status,
        reason=payload.reason,
        changed_by=current_user.id,
    )
    db.add(history)
    await db.commit()
    await db.refresh(tender)
    return tender


async def get_tender(db: AsyncSession, tender_id: int) -> Tender:
    return await _get_tender_or_404(db, tender_id)


async def list_tenders(db: AsyncSession, status_filter: TenderStatus | None = None) -> list[Tender]:
    stmt = select(Tender).order_by(Tender.id.desc())
    if status_filter is not None:
        stmt = stmt.where(Tender.status == status_filter)
    result = await db.scalars(stmt)
    return list(result.all())


async def get_history(db: AsyncSession, tender_id: int) -> list[TenderStatusHistory]:
    await _get_tender_or_404(db, tender_id)
    stmt = (
        select(TenderStatusHistory)
        .options(joinedload(TenderStatusHistory.changed_by_user))
        .where(TenderStatusHistory.tender_id == tender_id)
        .order_by(TenderStatusHistory.created_at.desc(), TenderStatusHistory.id.desc())
    )
    result = await db.scalars(stmt)
    return list(result.all())
