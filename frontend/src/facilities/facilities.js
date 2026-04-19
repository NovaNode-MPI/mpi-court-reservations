import { requireAuth, logout } from "../services/authGuard.js";
import { getFacilities } from "../services/facilitiesService.js";
import { createReservation } from "../services/myReservationsService.js";

requireAuth();

const loadingState = document.getElementById("loadingState");
const errorState = document.getElementById("errorState");
const emptyState = document.getElementById("emptyState");
const facilitiesGrid = document.getElementById("facilitiesGrid");
const retryButton = document.getElementById("retryButton");
const logoutLink = document.getElementById("logoutLink");
const searchInput = document.getElementById("searchInput");

const reservationModal = document.getElementById("reservationModal");
const modalOverlay = document.getElementById("modalOverlay");
const closeModalButton = document.getElementById("closeModalButton");
const cancelModalButton = document.getElementById("cancelModalButton");
const reservationForm = document.getElementById("reservationForm");
const facilityNameInput = document.getElementById("facilityNameInput");
const facilityIdInput = document.getElementById("facilityIdInput");
const reservationDateInput = document.getElementById("reservationDateInput");
const startSlotSelect = document.getElementById("startSlotSelect");
const durationSelect = document.getElementById("durationSelect");
const calculatedEndTime = document.getElementById("calculatedEndTime");
const calculatedPrice = document.getElementById("calculatedPrice");
const reservationFormMessage = document.getElementById("reservationFormMessage");

let facilitiesData = [];
let selectedFacilityForReservation = null;

logoutLink.addEventListener("click", (event) => {
  event.preventDefault();
  logout();
});

retryButton.addEventListener("click", loadFacilities);

searchInput.addEventListener("input", () => {
  const query = searchInput.value.toLowerCase().trim();

  const filtered = facilitiesData.filter((facility) =>
    (facility.name || "").toLowerCase().includes(query) ||
    (facility.type || "").toLowerCase().includes(query) ||
    (facility.location || "").toLowerCase().includes(query)
  );

  if (filtered.length === 0) {
    facilitiesGrid.innerHTML = "";
    loadingState.classList.add("hidden");
    errorState.classList.add("hidden");
    emptyState.classList.remove("hidden");
    facilitiesGrid.classList.add("hidden");
    return;
  }

  showSuccess(filtered);
});

modalOverlay.addEventListener("click", closeReservationModal);
closeModalButton.addEventListener("click", closeReservationModal);
cancelModalButton.addEventListener("click", closeReservationModal);

reservationDateInput.addEventListener("change", updateCalculatedReservationDetails);
startSlotSelect.addEventListener("change", updateCalculatedReservationDetails);
durationSelect.addEventListener("change", updateCalculatedReservationDetails);

async function loadFacilities() {
  showLoading();

  try {
    const facilities = await getFacilities();
    facilitiesData = facilities;

    if (facilities.length === 0) {
      showEmpty();
      return;
    }

    showSuccess(facilities);
  } catch (error) {
    showError();
  }
}

function showLoading() {
  loadingState.classList.remove("hidden");
  errorState.classList.add("hidden");
  emptyState.classList.add("hidden");
  facilitiesGrid.classList.add("hidden");
}

function showError() {
  loadingState.classList.add("hidden");
  errorState.classList.remove("hidden");
  emptyState.classList.add("hidden");
  facilitiesGrid.classList.add("hidden");
}

function showEmpty() {
  loadingState.classList.add("hidden");
  errorState.classList.add("hidden");
  emptyState.classList.remove("hidden");
  facilitiesGrid.classList.add("hidden");
}

function showSuccess(facilities) {
  loadingState.classList.add("hidden");
  errorState.classList.add("hidden");
  emptyState.classList.add("hidden");
  facilitiesGrid.classList.remove("hidden");

  renderFacilities(facilities);
}

function renderFacilities(facilities) {
  facilitiesGrid.innerHTML = "";

  facilities.forEach((facility) => {
    const card = document.createElement("div");
    card.className = "facility-card";

    const pricesHtml =
      facility.prices && facility.prices.length > 0
        ? facility.prices
            .map((priceItem) => `<li>${priceItem.duration} - ${priceItem.price} RON</li>`)
            .join("")
        : "<li>No pricing available.</li>";

    const imageHtml = facility.image_url
      ? `<img src="${facility.image_url}" alt="${facility.name}" />`
      : `<div class="facility-image-placeholder">No image</div>`;

    card.innerHTML = `
      <div class="card-inner">
        <div class="card-front">
          <div class="facility-image">
            ${imageHtml}
          </div>

          <div class="facility-info">
            <h3>${facility.name || "Unnamed facility"}</h3>
            <p><strong>Type:</strong> ${facility.type || "N/A"}</p>
            <p><strong>Location:</strong> ${facility.location || "N/A"}</p>
            <button class="info-button" type="button">More info</button>
          </div>
        </div>

        <div class="card-back">
          <h4>Pricing</h4>
          <ul>
            ${pricesHtml}
          </ul>

          <div class="card-back-buttons">
            <button class="book-button" type="button">Book now</button>
            <button class="back-button" type="button">Back</button>
          </div>
        </div>
      </div>
    `;

    const inner = card.querySelector(".card-inner");
    const infoBtn = card.querySelector(".info-button");
    const backBtn = card.querySelector(".back-button");
    const bookBtn = card.querySelector(".book-button");

    infoBtn.addEventListener("click", () => {
      inner.classList.add("flipped");
    });

    backBtn.addEventListener("click", () => {
      inner.classList.remove("flipped");
    });

    bookBtn.addEventListener("click", () => {
      openReservationModal(facility.id);
    });

    facilitiesGrid.appendChild(card);
  });
}

function openReservationModal(selectedFacilityId) {
  const selectedFacility = facilitiesData.find(
    (facility) => facility.id === selectedFacilityId
  );

  if (!selectedFacility) {
    showReservationFormMessage("Selected facility could not be found.", true);
    return;
  }

  selectedFacilityForReservation = selectedFacility;

  reservationForm.reset();
  clearReservationFormMessage();

  facilityIdInput.value = String(selectedFacility.id);
  facilityNameInput.value = selectedFacility.name || "Unnamed facility";

  populateStartSlotOptions();
  populateDurationOptions(selectedFacility);
  setDefaultReservationDate();
  updateCalculatedReservationDetails();

  reservationModal.classList.remove("hidden");
  reservationModal.setAttribute("aria-hidden", "false");
}

function closeReservationModal() {
  reservationModal.classList.add("hidden");
  reservationModal.setAttribute("aria-hidden", "true");

  reservationForm.reset();
  facilityIdInput.value = "";
  facilityNameInput.value = "";
  calculatedEndTime.value = "";
  calculatedPrice.value = "";
  selectedFacilityForReservation = null;

  clearReservationFormMessage();
}

function showReservationFormMessage(message, isError = false) {
  reservationFormMessage.textContent = message;
  reservationFormMessage.classList.remove("hidden");
  reservationFormMessage.classList.toggle("error-message", isError);
  reservationFormMessage.classList.toggle("success-message", !isError);
}

function clearReservationFormMessage() {
  reservationFormMessage.textContent = "";
  reservationFormMessage.classList.add("hidden");
  reservationFormMessage.classList.remove("error-message", "success-message");
}

function parseDurationToMinutes(durationText) {
  if (!durationText) {
    return 0;
  }

  const value = parseFloat(durationText);

  if (Number.isNaN(value)) {
    return 0;
  }

  const normalized = durationText.toLowerCase();

  if (normalized.includes("hour")) {
    return value * 60;
  }

  if (normalized.includes("min")) {
    return value;
  }

  return value;
}

function populateStartSlotOptions() {
  startSlotSelect.innerHTML = "";

  for (let hour = 0; hour < 24; hour += 1) {
    for (const minute of [0, 30]) {
      const hourText = String(hour).padStart(2, "0");
      const minuteText = String(minute).padStart(2, "0");
      const value = `${hourText}:${minuteText}`;

      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;

      startSlotSelect.appendChild(option);
    }
  }
}

function populateDurationOptions(facility) {
  durationSelect.innerHTML = "";

  if (!facility?.prices || facility.prices.length === 0) {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = "No durations available";
    durationSelect.appendChild(option);
    return;
  }

  facility.prices.forEach((priceItem, index) => {
    const option = document.createElement("option");
    option.value = String(index);
    option.textContent = `${priceItem.duration} - ${priceItem.price} RON`;
    durationSelect.appendChild(option);
  });
}

function setDefaultReservationDate() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");

  reservationDateInput.value = `${year}-${month}-${day}`;
}

function updateCalculatedReservationDetails() {
  if (!selectedFacilityForReservation) {
    calculatedEndTime.value = "";
    calculatedPrice.value = "";
    return;
  }

  const dateValue = reservationDateInput.value;
  const startSlotValue = startSlotSelect.value;
  const durationIndex = Number(durationSelect.value);

  if (!dateValue || !startSlotValue || Number.isNaN(durationIndex)) {
    calculatedEndTime.value = "";
    calculatedPrice.value = "";
    return;
  }

  const selectedPrice = selectedFacilityForReservation.prices?.[durationIndex];

  if (!selectedPrice) {
    calculatedEndTime.value = "";
    calculatedPrice.value = "";
    return;
  }

  const startDate = new Date(`${dateValue}T${startSlotValue}`);
  const durationMinutes = parseDurationToMinutes(selectedPrice.duration);

  if (Number.isNaN(startDate.getTime()) || durationMinutes <= 0) {
    calculatedEndTime.value = "";
    calculatedPrice.value = "";
    return;
  }

  const endDate = new Date(startDate.getTime() + durationMinutes * 60 * 1000);

  calculatedEndTime.value = endDate.toLocaleString();
  calculatedPrice.value = `${selectedPrice.price} RON`;
}

reservationForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearReservationFormMessage();

  const facilityId = Number(facilityIdInput.value);
  const dateValue = reservationDateInput.value;
  const startSlotValue = startSlotSelect.value;
  const durationIndex = Number(durationSelect.value);

  if (!facilityId) {
    showReservationFormMessage("Facility could not be selected.", true);
    return;
  }

  if (!dateValue || !startSlotValue || Number.isNaN(durationIndex)) {
    showReservationFormMessage("Please complete all fields.", true);
    return;
  }

  const selectedPrice = selectedFacilityForReservation?.prices?.[durationIndex];

  if (!selectedPrice) {
    showReservationFormMessage("Selected duration is invalid.", true);
    return;
  }

  const startDate = new Date(`${dateValue}T${startSlotValue}`);
  const durationMinutes = parseDurationToMinutes(selectedPrice.duration);
  const endDate = new Date(startDate.getTime() + durationMinutes * 60 * 1000);

  if (Number.isNaN(startDate.getTime()) || Number.isNaN(endDate.getTime())) {
    showReservationFormMessage("Invalid date or time.", true);
    return;
  }

  if (startDate >= endDate) {
    showReservationFormMessage("Start time must be earlier than end time.", true);
    return;
  }

  try {
    await createReservation({
      facility_id: facilityId,
      start_time: startDate.toISOString(),
      end_time: endDate.toISOString(),
    });

    showReservationFormMessage(
      "Reservation created successfully. You can view it in My Reservations.",
      false
    );

    setTimeout(() => {
      closeReservationModal();
      window.location.href = "/myReservations.html";
    }, 1200);
  } catch (error) {
    console.log(error);
    console.log(error?.status);
    console.log(error?.message);

    if (error?.status === 409) {
      showReservationFormMessage("Time slot already booked.", true);
      return;
    }

    showReservationFormMessage(
      error?.message || "Could not create reservation. Please try again.",
      true
    );
  }
});

loadFacilities();