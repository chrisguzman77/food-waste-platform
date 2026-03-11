from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.enums import DeliveryStatus, DonationStatus, UserRole
from app.models.delivery import Delivery
from app.models.donation import Donation
from app.models.user import User


class DeliveryService:
    @staticmethod
    def list_open_deliveries(db: Session) -> list[Delivery]:
        result = db.scalars(select(Delivery).where(Delivery.status == DeliveryService.OPEN))
        return list(result)
    
    @staticmethod
    def claim_delivery(db: Session, *, delivery_id: int, current_user: User) -> Delivery:
        if current_user.role != UserRole.VOLUNTEER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only volunteers can claim deliveries")
        
        delivery = db.scalar(select(Delivery).where(Delivery.id == delivery_id))
        if not delivery:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")
        if delivery.status != DeliveryStatus.OPEN:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delivery already claimed")
        
        delivery.volunteer_user_id = current_user.id
        delivery.assigned_at = datetime.now(UTC)
        delivery.status = DeliveryStatus.ASSIGNED
        db.flush()
        return delivery
    
    @staticmethod
    def update_status(db: Session, *, delvery_id: int, new_status: DeliveryStatus, current_user: User) -> Delivery:
        delivery = db.scalar(select(Delivery).where(Delivery.id == delvery_id))
        if not delivery:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")
        if current_user.role not in {UserRole.VOLUNTEER, UserRole.ADMIN}:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only volunteers or admins can update delivery status")
        
        donation = db.scalar(select(Donation).where(Donation.id == delivery.donation_id))
        if not donation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Related donation not found")
        
        now = datetime.now(UTC)
        delivery.status = new_status

        if new_status == DeliveryStatus.EN_ROUTE_PICKUP:
            pass
        elif new_status == DeliveryStatus.PICKED_UP:
            delivery.picked_up_at = now
            donation.status = DonationStatus.DELIVERED
        elif new_status == DeliveryStatus.DELIVERED:
            delivery.delivered_at = now
            donation.status = DonationStatus.DELIVERED

        db.flush()
        return delivery