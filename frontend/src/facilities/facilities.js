import { requireAuth, logout } from "../services/authGuard.js";
import { getFacilities } from "../services/facilitiesService.js";

requireAuth();

const loadingState = document.getElementById("loadingState");
const errorState = document.getElementById("errorState");
const emptyState = document.getElementById("emptyState");
const facilitiesGrid = document.getElementById("facilitiesGrid");
const retryButton = document.getElementById("retryButton");
const logoutButton = document.getElementById("logoutButton");
const accountButton = document.getElementById("accountButton");
const searchInput = document.getElementById("searchInput");

let facilitiesData = [];

logoutButton.addEventListener("click", logout);

accountButton.addEventListener("click", () => {
  alert("Account page will be added later.");
});

retryButton.addEventListener("click", loadFacilities);

searchInput.addEventListener("input", () => {
  const query = searchInput.value.toLowerCase().trim();

  const filtered = facilitiesData.filter((facility) =>
    facility.name.toLowerCase().includes(query) ||
    facility.type.toLowerCase().includes(query) ||
    facility.location.toLowerCase().includes(query)
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

    card.innerHTML = `
      <div class="card-inner">
        <div class="card-front">
          <div class="facility-image">
            ${
              facility.image_url
                ? `<img src="${facility.image_url}" alt="${facility.name}" />`
                : "No image"
            }
          </div>

          <div class="facility-info">
            <h3>${facility.name}</h3>
            <p><strong>Type:</strong> ${facility.type}</p>
            <p><strong>Location:</strong> ${facility.location}</p>
            <button class="info-button">More info</button>
          </div>
        </div>

        <div class="card-back">
          <h4>Pricing</h4>
          <ul>
            ${
              facility.prices?.map(
                (p) => `<li>${p.duration} - ${p.price} RON</li>`
              ).join("") || "<li>No pricing available.</li>"
            }
          </ul>

          <div class="card-back-buttons">
            <button class="book-button">Book now</button>
            <button class="back-button">Back</button>
          </div>
        </div>
      </div>
    `;

    const inner = card.querySelector(".card-inner");
    const infoBtn = card.querySelector(".info-button");
    const backBtn = card.querySelector(".back-button");

    infoBtn.addEventListener("click", () => {
      inner.classList.add("flipped");
    });

    backBtn.addEventListener("click", () => {
      inner.classList.remove("flipped");
    });

    facilitiesGrid.appendChild(card);
  });
}

loadFacilities();