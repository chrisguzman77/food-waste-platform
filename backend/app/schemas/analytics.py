from pydantic import BaseModel


class PlatformAnalyticsResponse(BaseModel):
    total_donations: int
    total_units_donated: int
    total_deliveries_completed: int
    estimated_meals_saved: int