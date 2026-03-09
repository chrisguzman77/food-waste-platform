from enum import StrEnum


class UserRole(StrEnum):
    RESTAURANT = "restaurant"
    FOOD_BANK = "food_bank"
    VOLUNTEER = "volunteer"
    ADMIN = "admin"


class OrganizationType(StrEnum):
    RESTAURANT = "restaurant"
    FOOD_BANK = "food_bank"


class DonationStatus(StrEnum):
    AVAILABLE = "available"
    CLAIMED = "claimed"
    NEEDS_VOLUNTEER = "needs_volunteer"
    PICKED_UP = "picked_up"
    DELIVERED = "delivered"
    CANCELED = "canceled"
    EXPIRED = "expired"


class DeliveryStatus(StrEnum):
    OPEN = "open"
    ASSIGNED = "assigned"
    EN_ROUTE_PICKUP = "en_route_pickup"
    PICKED_UP = "picked_up"
    DELIVERED = "delivered"


class NotificationType(StrEnum):
    NEW_DONATION = "new_donation"
    DONATION_CLAIMED = "donation_claimed"
    VOLUNTEER_REQUESTED = "volunteer_requested"
    DELIVERY_ASSIGNED = "delivery_assigned"
    DELIVERY_COMPLETED = "delivery_completed"