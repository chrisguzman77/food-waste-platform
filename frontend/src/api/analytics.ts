import { apiClient } from "./client";

export interface PlatformAnalytics {
    total_donations: number;
    total_units_donated: number;
    total_deliveries_completed: number;
    estimated_meals_saved: number;
    claimed_donations: number;
    pending_verifications: number;
}

export interface RestaurantAnalytics {
    total_donations_created: number;
    delivered_donations: number;
    total_units_donated: number;
    estimated_meals_donated: number;
}

export interface FoodBankAnalytics {
    total_donations_claimed: number;
    delivered_donations_received: number;
    total_units_received: number;
}

export interface VolunteerAnalytics {
    routes_claimed: number;
    routes_completed: number;
}

export function getPlatformAnalytics() {
    return apiClient.get<PlatformAnalytics>("/analytics/platform");
}

export function getRestaurantAnalytics() {
    return apiClient.get<RestaurantAnalytics>("/analytics/restaurant/me");
}

export function getFoodBankAnalytics() {
    return apiClient.get<FoodBankAnalytics>("/analytics/foodbank/me");
}

export function getVolunteerAnalytics() {
    return apiClient.get<VolunteerAnalytics>("/analytics/volunteer/me")
}