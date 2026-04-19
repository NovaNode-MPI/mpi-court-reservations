import { requireAuth, logout } from "../services/authGuard.js";
import { getMyReservations } from "../services/myReservationsService.js";

requireAuth();

const logoutLink = document.getElementById("logoutLink");
const loadingState = document.getElementById("loadingState");
const errorState = document.getElementById("errorState");
const emptyState = document.getElementById("emptyState");
const reservationsList = document.getElementById("reservationsList");
const retryButton = document.getElementById("retryButton");

logoutLink.addEventListener("click", (event) => {
  event.preventDefault();
  logout();
});

retryButton.addEventListener("click", loadReservations);

function formatDateTime(value) {
  if (!value) {
    return "N/A";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "Invalid date";
  }

  return date.toLocaleString();
}

function showLoading() {
  loadingState.classList.remove("hidden");
  errorState.classList.add("hidden");
  emptyState.classList.add("hidden");
  reservationsList.classList.add("hidden");
}

function showError() {
  loadingState.classList.add("hidden");
  errorState.classList.remove("hidden");
  emptyState.classList.add("hidden");
  reservationsList.classList.add("hidden");
}

function showEmpty() {
  loadingState.classList.add("hidden");
  errorState.classList.add("hidden");
  emptyState.classList.remove("hidden");
  reservationsList.classList.add("hidden");
}

function showSuccess(reservations) {
  loadingState.classList.add("hidden");
  errorState.classList.add("hidden");
  emptyState.classList.add("hidden");
  reservationsList.classList.remove("hidden");

  renderReservations(reservations);
}

function renderReservations(reservations) {
  reservationsList.innerHTML = "";

  reservations.forEach((reservation) => {
    const card = document.createElement("article");
    card.className = "reservation-card";

    card.innerHTML = `
      <h3>Reservation #${reservation.id}</h3>
      <p><strong>Facility ID:</strong> ${reservation.facility_id}</p>
      <p><strong>Start:</strong> ${formatDateTime(reservation.start_time)}</p>
      <p><strong>End:</strong> ${formatDateTime(reservation.end_time)}</p>
      <p><strong>Status:</strong> ${reservation.status}</p>
    `;

    reservationsList.appendChild(card);
  });
}

async function loadReservations() {
  showLoading();

  try {
    const reservations = await getMyReservations();

    if (!reservations || reservations.length === 0) {
      showEmpty();
      return;
    }

    showSuccess(reservations);
  } catch (error) {
    showError();
  }
}

loadReservations();