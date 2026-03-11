from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.enums import DeliveryStatus, DonationStatus
from app.models.delivery import Delivery
from app.models.donation import Donation


class AnalyticsService:
    @staticmethod
    def platform_summary(db: Session) -> dict[str, int]:
        total_donations = db.scalar(select(func.count(Donation.id))) or 0
        total_units = db.scalar(select(func.coalesce(func.sum(Donation.quantity), 0))) or 0
        completed_deliveries = (
            db.scalar(select(func.count(Delivery.id)).where(Delivery.status == DeliveryStatus.DELIVERED)) or 0
        )
        delivered_quantity = (
            db.scalar(
                select(func.coalesce(func.sum(Donation.quantity), 0)).where(
                    Donation.status == DonationStatus.DELIVERED
                )
            )
            or 0
        )

        estimated_meals_saved = int(delivered_quantity * 2)

        return {
            "total_donations": int(total_donations),
            "total_units_donated": int(total_units),
            "total_deliveries_completed": int(completed_deliveries),
            "estimated_meals_saved": int(estimated_meals_saved),
        }