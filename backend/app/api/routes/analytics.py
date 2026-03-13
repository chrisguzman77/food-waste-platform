from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.analytics import(
    FoodBankAnalyticsResponse,
    PlatformAnalyticsResponse,
    RestaurantAnalyticsResponse,
    VolunteerAnalyticsResponse,
)
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/platform", response_model=PlatformAnalyticsResponse)
def get_platform_analytics(db: Session = Depends(get_db)) -> PlatformAnalyticsResponse:
    return PlatformAnalyticsResponse(**AnalyticsService.platform_summary(db))

@router.get("/restaurant/me", response_model=RestaurantAnalyticsResponse)
def get_restaurant_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RestaurantAnalyticsResponse:
    return RestaurantAnalyticsResponse(**AnalyticsService.restaurant_summary(db, current_user.id))

@router.get("/foodbank/me", response_model=FoodBankAnalyticsResponse)
def get_food_bank_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FoodBankAnalyticsResponse:
    return FoodBankAnalyticsResponse(**AnalyticsService.food_bank_summary(db, current_user.id))

@router.get("/volunteer/me", response_model=VolunteerAnalyticsResponse)
def get_volunteer_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> VolunteerAnalyticsResponse:
    return VolunteerAnalyticsResponse(**AnalyticsService.volunteer_summary(db, current_user.id))