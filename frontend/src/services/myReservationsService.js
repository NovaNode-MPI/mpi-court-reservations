import { API_BASE_URL } from "../config.js";
import { getToken, logout } from "./authGuard.js";

export async function getMyReservations() {
  const token = getToken();

  const response = await fetch(`${API_BASE_URL}/reservations`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

  if (response.status === 401) {
    logout();
    return;
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.detail || "Failed to load reservations");
  }

  return data;
}

export async function createReservation(payload) {
  const token = getToken();

  const response = await fetch(`${API_BASE_URL}/reservations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });

  if (response.status === 401) {
    logout();
    return;
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const error = new Error(data?.detail || "Failed to create reservation");
    error.status = response.status;
    throw error;
  }

  return data;
}