from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models import TenderStatus, User
from app.schemas.tender import TenderCreate, TenderRead, TenderStatusHistoryRead, TenderStatusUpdate
from app.services import tender as tender_service

router = APIRouter(prefix="/tenders", tags=["tenders"])


@router.post("", response_model=TenderRead, status_code=status.HTTP_201_CREATED)
async def create_tender(
    payload: TenderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await tender_service.create_tender(db, payload, current_user)


@router.get("", response_model=list[TenderRead])
async def list_tenders(
    status_filter: TenderStatus | None = Query(default=None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await tender_service.list_tenders(db, status_filter)


@router.get("/{tender_id}", response_model=TenderRead)
async def get_tender(
    tender_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await tender_service.get_tender(db, tender_id)


@router.patch("/{tender_id}/status", response_model=TenderRead)
async def update_status(
    tender_id: int,
    payload: TenderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await tender_service.update_tender_status(db, tender_id, payload, current_user)


@router.get("/{tender_id}/history", response_model=list[TenderStatusHistoryRead])
async def get_history(
    tender_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await tender_service.get_history(db, tender_id)
