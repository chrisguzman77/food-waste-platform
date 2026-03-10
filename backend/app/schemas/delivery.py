from datetime import datetime

from pydantic import BaseModel

from app.core.enums import DeliveryStatus


class DeliveryResponse(BaseModel):
    id: int
    donation_id: int
    volunteer_user_id: int | None
    pickup_org_id: int
    dropoff_org_id: int
    assigned_at: datetime | None
    picked_up_at: datetime | None
    delivered_at: datetime | None
    status: DeliveryStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class DeliveryClaimRequest(BaseModel):
    pass


class DeliveryStatusUpdate(BaseModel):
    status: DeliveryStatus