from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.organization import Organization
from app.models.user import User
from app.schemas.organization import OrganizationCreate, OrganizationResponse

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(
    payload: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Organization:
    organization = Organization(
        name=payload.name,
        type=payload.type,
        address=payload.address,
        latitude=payload.latitude,
        longitude=payload.longitude,
        phone=payload.phone,
        verified=current_user.role == "admin",
        created_by_user_id=current_user.id,
    )
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization