import { API_BASE_URL } from "../lib/constants";
import { getAccessToken } from "../lib/storage";

export class ApiError extends Error {
    status: number;

    constructor(message: string, status: number) {
        super(message);
        this.status = status;
    }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const token = getAccessToken();

    const headers = new Headers(options.headers || {});
    headers.set("Content-Type", "application/json");
    if (token) {
        headers.set("Authorization", 'Bearer ${token}');
    }

    const response = await fetch('${API_BASE_URL}${path}', {
        ...options,
        headers,
    });
    const text = await response.text();
    const data = text ? JSON.parse(text) : null;

    if (!response.ok) {
        throw new ApiError(data?.detail || "Request failed", response.status);
    }

    return data as T;
}

export const apiClient = {
    get: <T>(path: string) => request<T>(path, { method: "GET"}),
    post: <T>(path: string, body?: unknown) => 
        request<T>(path, { method: "POST", body: body ? JSON.stringify(body) : undefined }),
    patch: <T>(path: string, body?: unknown) =>
        request<T>(path, { method: "PATCH", body: body ? JSON.stringify(body) : undefined}),
};