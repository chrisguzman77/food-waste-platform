from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.delivery import DeliveryResponse, DeliveryStatusUpdate
from app.services.delivery_service import DeliveryService

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.get("/open", response_model=list[DeliveryResponse])
def list_open_deliveries(db: Session = Depends(get_db)):
    return DeliveryService.list_open_deliveries(db)


@router.post("/{delivery_id}/claim", response_model=DeliveryResponse)
def claim_delivery(
    delivery_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delivery = DeliveryService.claim_delivery(db, delivery_id=delivery_id, current_user=current_user)
    db.commit()
    db.refresh(delivery)
    return delivery


@router.patch("/{delivery_id}/status", response_model=DeliveryResponse)
def update_delivery_status(
    delivery_id: int,
    payload: DeliveryStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    delivery = DeliveryService.update_status(
        db,
        delivery_id=delivery_id,
        new_status=payload.status,
        current_user=current_user,
    )
    db.commit()
    db.refresh(delivery)
    return delivery