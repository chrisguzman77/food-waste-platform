from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.analytics import PlatformAnalyticsResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/platform", response_model=PlatformAnalyticsResponse)
def get_platform_analytics(db: Session = Depends(get_db)) -> PlatformAnalyticsResponse:
    return PlatformAnalyticsResponse(**AnalyticsService.platform_summary(db))