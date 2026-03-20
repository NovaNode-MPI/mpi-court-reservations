import { USE_MOCK_API, API_BASE_URL } from "../config.js";

const mockFacilities = [
  {
    id: 1,
    name: "Tennis Court",
    type: "Court",
    location: "Cluj-Napoca, Central Sports Base",
    image_url: "",
    prices: [
      { duration: "1 hour", price: 80 },
      { duration: "2 hours", price: 150 }
    ]
  }
];

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function mockGetFacilities() {
  await wait(800);
  return mockFacilities;
}

async function realGetFacilities() {
  const response = await fetch(`${API_BASE_URL}/facilities`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json"
    }
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.detail || "Failed to load facilities");
  }

  return data;
}

export async function getFacilities() {
  if (USE_MOCK_API) {
    return mockGetFacilities();
  }

  return realGetFacilities();
}