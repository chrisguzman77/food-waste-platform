from datetime import datetime

from pydantic import BaseModel

from app.core.enums import NotificationType


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: NotificationType
    title: str
    message: str
    read: bool
    created_at: datetime

    model_config = {"from_attributes": True}
    