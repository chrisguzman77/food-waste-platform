from sqlalchemy.orm import Session

from app.core.enums import NotificationType
from app.models.notification import Notification


class NotificationService:
    @staticmethod
    def create_notification(
        db: Session,
        *,
        user_id: int,
        type_:NotificationType,
        title: str,
        message: str,
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            type=type_,
            title=title,
            message=message,
            read=False,
        )
        db.add(notification)
        db.flush()
        return notification