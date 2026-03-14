export type UserRole = "restaurant" | "food_bank" | "volunteer" | "admin";

export interface User {
  id: number;
  full_name: string;
  email: string;
  role: UserRole;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface Organization {
  id: number;
  name: string;
  type: "restaurant" | "food_bank";
  address: string;
  latitude: number;
  longitude: number;
  phone: string | null;
  verified: boolean;
  created_by_user_id: number;
  created_at: string;
}

export interface Donation {
  id: number;
  organization_id: number;
  title: string;
  description: string;
  food_type: string;
  quantity: number;
  unit: string;
  prepared_at: string;
  expires_at: string;
  pickup_deadline: string;
  location_address: string;
  latitude: number;
  longitude: number;
  special_handling: string | null;
  status:
    | "available"
    | "claimed"
    | "needs_volunteer"
    | "picked_up"
    | "delivered"
    | "canceled"
    | "expired";
  claimed_by_org_id: number | null;
  created_at: string;
}

export interface Delivery {
  id: number;
  donation_id: number;
  volunteer_user_id: number | null;
  pickup_org_id: number;
  dropoff_org_id: number;
  assigned_at: string | null;
  picked_up_at: string | null;
  delivered_at: string | null;
  status: "open" | "assigned" | "en_route_pickup" | "picked_up" | "delivered";
  created_at: string;
}

export interface NotificationItem {
  id: number;
  user_id: number;
  type: string;
  title: string;
  message: string;
  read: boolean;
}