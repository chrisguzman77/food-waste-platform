from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import ClaimDonationRequest, DonationCreate, DonationResponse
from app.services.donation_service import DonationService

router = APIRouter(prefix="/donations", tags=["donations"])


@router.post("", response_model=DonationResponse, status_code=status.HTTP_201_CREATED)
def create_donation(
    payload: DonationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Donation:
    donation = DonationService.create_donation(db, payload=payload, current_user=current_user)
    db.commit()
    db.refresh(donation)
    return donation


@router.get("", response_model=list[DonationResponse])
def list_donations(db: Session= Depends(get_db)) -> list[Donation]:
    return DonationService.list_available_donations(db)


@router.get("/{donation_id}", response_model=DonationResponse)
def get_donation(donation_id: int, db: Session = Depends(get_db)) -> Donation:
    donation = db.scalar(select(Donation).where(Donation.id == donation_id))
    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")
    return donation


@router.post("/{donation_id}/claim", response_model=DonationResponse)
def claim_donation(
    donation_id: int,
    payload: ClaimDonationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Donation:
    donation = DonationService.claim_donation(
        db,
        donation_id=donation_id,
        payload=payload,
        current_user=current_user,
    )
    db.commit()
    db.refresh(donation)
    return donation