from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.enums import DeliveryStatus, DonationStatus, NotificationType, OrganizationType, UserRole
from app.models.delivery import Delivery
from app.models.donation import Donation
from app.models.organization import Organization
from app.models.user import User
from app.schemas.donation import ClaimDonationRequest, DonationCreate
from app.services.notification_service import NotificationService


class DonationService:
    @staticmethod
    def create_donation(db: Session, *, payload: DonationCreate, current_user: User) -> Donation:
        if current_user.role != UserRole.RESTAURANT:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only restaurants can create donations")
        
        organization = db.scalar(
            select(Organization).where(
                Organization.id == payload.organization_id, 
                Organization.created_by_user_id == current_user.id,
                Organization.type == OrganizationType.RESTAURANT,
            )
        )
        if not organization:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant organization not found")
        
        donation = Donation(
            organization_id=payload.organization_id,
            title=payload.title,
            description=payload.description,
            food_type=payload.food_type,
            quantity=payload.quantity,
            unit=payload.unit,
            prepared_at=payload.prepared_at,
            expires_at=payload.expires_at,
            pickup_deadline=payload.pickup_deadline,
            location_address=payload.location_address,
            latitude=payload.latitude,
            longitude=payload.longitude,
            special_handling=payload.special_handling,
            status=DonationStatus.AVAILABLE,
        )
        db.add(donation)
        db.flush()
        return donation
    
    @staticmethod
    def list_available_donations(db: Session) -> list[Donation]:
        now = datetime.now(UTC)
        result = db.scalars(
            select(Donation).where(
                Donation.status.in_([DonationStatus.AVAILABLE, DonationStatus.NEEDS_VOLUNTEER]),
                Donation.pickup_deadline >= now,
            )
        )
        return list(result)

    @staticmethod
    def claim_donation(
        db: Session,
        *,
        donation_id: int,
        payload: ClaimDonationRequest,
        current_user: User,
    ) -> Donation:
        if current_user.role != UserRole.FOOD_BANK:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only food banks can claim donations")

        donation = db.scalar(select(Donation).where(Donation.id == donation_id))
        if not donation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")
        if donation.status != DonationStatus.AVAILABLE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Donation is no longer available")

        food_bank = db.scalar(
            select(Organization).where(
                Organization.id == payload.recipient_organization_id,
                Organization.created_by_user_id == current_user.id,
                Organization.type == OrganizationType.FOOD_BANK,
            )
        )
        if not food_bank:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Food bank organization not found")

        donation.claimed_by_org_id = food_bank.id
        donation.status = DonationStatus.NEEDS_VOLUNTEER if payload.needs_volunteer else DonationStatus.CLAIMED

        donor_org = db.scalar(select(Organization).where(Organization.id == donation.organization_id))
        if donor_org:
            donor_user = db.scalar(select(User).where(User.id == donor_org.created_by_user_id))
            if donor_user:
                NotificationService.create_notification(
                    db,
                    user_id=donor_user.id,
                    type_=NotificationType.DONATION_CLAIMED,
                    title="Donation claimed",
                    message=f"Your donation '{donation.title}' was claimed by {food_bank.name}.",
                )

        if payload.needs_volunteer:
            delivery = Delivery(
                donation_id=donation.id,
                volunteer_user_id=None,
                pickup_org_id=donation.organization_id,
                dropoff_org_id=food_bank.id,
                status=DeliveryStatus.OPEN,
            )
            db.add(delivery)

        db.flush()
        return donation