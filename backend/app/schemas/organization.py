from datetime import datetime

from pydantic import BaseModel, Field

from app.core.enums import OrganizationType


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    type: OrganizationType
    address: str = Field(min_length=5, max_length=255)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    phone: str | None = Field(default=None, max_length=50)


class OrganizationResponse(BaseModel):
    id: int
    name: str
    type: OrganizationType
    address: str
    latitude: float
    longitude: float
    phone: str | None
    verified: bool
    created_by_user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


