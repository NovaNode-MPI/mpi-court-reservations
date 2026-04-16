import { requireAuth, logout } from "../services/authGuard.js";

requireAuth();

const logoutLink = document.getElementById("logoutLink");

logoutLink.addEventListener("click", (event) => {
  event.preventDefault();
  logout();
});