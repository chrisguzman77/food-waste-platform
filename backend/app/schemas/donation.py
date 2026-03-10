from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.core.enums import DonationStatus


class DonationCreate(BaseModel):
    organization_id: int
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=5)
    food_type: str = Field(min_length=2, max_length=100)
    quantity: int = Field(gt=0)
    unit: str = Field(min_length=1, max_length=50)
    prepared_at: datetime
    expires_at: datetime
    pickup_deadline: datetime
    location_address: str = Field(min_length=5, max_length=255)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    special_handling: str | None = None

    @model_validator(mode="after")
    def validate_times(self) -> "DonationCreate":
        if self.expires_at <= self.prepared_at:
            raise ValueError("expires_at must be after prepare_at")
        if self.pickup_deadline > self.expires_at:
            raise ValueError("pickup_deadline cannot be after expires_at")
        return self
    

class DonationResponse(BaseModel):
    id: int
    organization_id: int
    title: str
    description: str
    food_type: str
    quantity: int
    unit: str
    prepared_at: datetime
    expires_at: datetime
    pickup_deadline: datetime
    location_address: str
    latitude: float
    longitude: float
    special_handling: str | None
    status: DonationStatus
    claimed_by_org_id: int | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ClaimDonationRequest(BaseModel):
    recipient_organization_id: int
    needs_volunteer: bool = False